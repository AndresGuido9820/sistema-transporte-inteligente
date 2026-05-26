from __future__ import annotations

from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from .common import DATA_DIR, MODELS_DIR, OUTPUTS_DIR, ensure_dirs, write_json


def image_features(path: str | Path) -> np.ndarray:
    path = Path(path)
    if not path.is_absolute():
        path = DATA_DIR.parents[0] / path
    image = Image.open(path).convert("RGB").resize((64, 64))
    arr = np.asarray(image, dtype=float) / 255.0
    means = arr.mean(axis=(0, 1))
    stds = arr.std(axis=(0, 1))
    dark_ratio = float((arr.mean(axis=2) < 0.2).mean())
    return np.concatenate([means, stds, [dark_ratio]])


def train_vision_model(input_path: Path | None = None) -> dict[str, float]:
    ensure_dirs()
    input_path = input_path or DATA_DIR / "processed" / "driver_images.csv"
    data = pd.read_csv(input_path)
    x = np.vstack([image_features(path) for path in data["image_path"]])
    y = data["label"].to_numpy()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    report = classification_report(y_test, pred, output_dict=True, zero_division=0)
    metrics = {
        "accuracy": float(accuracy_score(y_test, pred)),
        "macro_precision": float(report["macro avg"]["precision"]),
        "macro_recall": float(report["macro avg"]["recall"]),
        "macro_f1": float(report["macro avg"]["f1-score"]),
    }
    write_json(OUTPUTS_DIR / "metrics" / "vision_metrics.json", metrics)
    ConfusionMatrixDisplay.from_predictions(y_test, pred, xticks_rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "figures" / "vision_confusion_matrix.png")
    plt.close()
    joblib.dump(model, MODELS_DIR / "vision_model.joblib")
    return metrics


def classify_image(path: str | Path) -> dict[str, float | str]:
    model_path = MODELS_DIR / "vision_model.joblib"
    if not model_path.exists():
        train_vision_model()
    model = joblib.load(model_path)
    features = image_features(path).reshape(1, -1)
    label = str(model.predict(features)[0])
    confidence = float(model.predict_proba(features).max()) if hasattr(model, "predict_proba") else 1.0
    result: dict[str, float | str] = {"label": label, "confidence": confidence}
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(features)[0]
        for class_name, probability in zip(model.classes_, probabilities):
            result[f"probability_{class_name}"] = float(probability)
    return result

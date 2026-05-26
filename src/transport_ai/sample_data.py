from __future__ import annotations

from pathlib import Path
import shutil

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

from .common import DATA_DIR, ensure_dirs


def prepare_public_transport_ai_demand() -> Path:
    """Backward-compatible wrapper that prepares the CTA bus ridership dataset."""
    return prepare_cta_bus_ridership()


def prepare_cta_bus_ridership() -> Path:
    """Download the complete CTA daily bus ridership by route dataset."""
    ensure_dirs()
    url = (
        "https://data.cityofchicago.org/resource/jyb9-n7fm.csv?"
        "$select=route,date,daytype,rides&$limit=1500000"
    )
    output_path = DATA_DIR / "processed" / "cta_bus_ridership_daily_by_route.csv"

    try:
        raw = pd.read_csv(url)
    except Exception:
        fallback = Path(__file__).resolve().parents[2] / "data" / "processed" / "cta_bus_ridership_daily_by_route.csv"
        if fallback.exists() and fallback != output_path:
            output_path.write_bytes(fallback.read_bytes())
            return output_path
        raise

    raw.to_csv(output_path, index=False)
    return output_path


def generate_recommendations(seed: int = 42) -> Path:
    ensure_dirs()
    rng = np.random.default_rng(seed)
    users = [f"U{i:03d}" for i in range(1, 81)]
    destinations = [
        ("Medellin", "urbano"),
        ("Bogota", "negocios"),
        ("Cartagena", "playa"),
        ("Santa Marta", "playa"),
        ("Manizales", "montana"),
        ("Pereira", "cafetero"),
        ("Cali", "urbano"),
        ("Guatape", "turismo"),
        ("Villa de Leyva", "cultural"),
        ("San Andres", "playa"),
    ]
    rows = []
    for user in users:
        preferred = rng.choice(["urbano", "playa", "montana", "cafetero", "cultural", "turismo", "negocios"])
        for dest, category in destinations:
            base = 0.72 if category == preferred else 0.24
            if rng.random() < base:
                rating = int(np.clip(rng.normal(4.4 if category == preferred else 3.4, 0.7), 1, 5))
                rows.append({"user_id": user, "destination": dest, "category": category, "rating": rating})
    path = DATA_DIR / "processed" / "travel_interactions.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def prepare_travel_recommendation_dataset(raw_dir: Path | None = None) -> Path | None:
    raw_dir = raw_dir or DATA_DIR / "raw" / "travel_recommendation"
    destinations_path = raw_dir / "Expanded_Destinations.csv"
    history_path = raw_dir / "Final_Updated_Expanded_UserHistory.csv"
    if not destinations_path.exists() or not history_path.exists():
        return None
    destinations = pd.read_csv(destinations_path)
    history = pd.read_csv(history_path)
    merged = history.merge(destinations, on="DestinationID", how="left")
    interactions = merged.rename(
        columns={
            "UserID": "user_id",
            "Name": "destination",
            "Type": "category",
            "ExperienceRating": "rating",
        }
    )[["user_id", "destination", "category", "rating"]]
    interactions["user_id"] = "U" + interactions["user_id"].astype(str).str.zfill(4)
    path = DATA_DIR / "processed" / "travel_interactions.csv"
    interactions.to_csv(path, index=False)
    return path


def generate_driver_images(seed: int = 42) -> Path:
    ensure_dirs()
    rng = np.random.default_rng(seed)
    out_dir = DATA_DIR / "processed" / "driver_images"
    out_dir.mkdir(parents=True, exist_ok=True)
    classes = {
        "normal": "#4C78A8",
        "telefono": "#F58518",
        "somnolencia": "#54A24B",
        "mirando_lado": "#B279A2",
    }
    rows = []
    for label, color in classes.items():
        for idx in range(18):
            image = np.ones((64, 64, 3), dtype=float)
            rgb = tuple(int(color[i : i + 2], 16) / 255 for i in (1, 3, 5))
            image[:, :] = rgb
            noise = rng.normal(0, 0.08, image.shape)
            image = np.clip(image + noise, 0, 1)
            marker_x = {"normal": 14, "telefono": 42, "somnolencia": 30, "mirando_lado": 50}[label]
            image[22:42, marker_x - 4 : marker_x + 4, :] = 0.05
            file_path = out_dir / f"{label}_{idx:02d}.png"
            plt.imsave(file_path, image)
            rows.append({"image_path": str(file_path), "label": label})
    manifest = DATA_DIR / "processed" / "driver_images.csv"
    pd.DataFrame(rows).to_csv(manifest, index=False)
    return manifest


def prepare_driver_behavior_dataset(raw_dir: Path | None = None, per_class: int = 40) -> Path | None:
    raw_dir = raw_dir or DATA_DIR / "raw" / "driver_behavior" / "Multi-Class Driver Behavior Image Dataset"
    if not raw_dir.exists():
        return None
    out_dir = DATA_DIR / "processed" / "driver_images_real"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for class_dir in sorted(path for path in raw_dir.iterdir() if path.is_dir()):
        image_paths = sorted(
            p for p in class_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
        )[:per_class]
        for idx, source in enumerate(image_paths):
            target = out_dir / f"{class_dir.name}_{idx:03d}.jpg"
            try:
                Image.open(source).convert("RGB").resize((96, 96)).save(target, quality=85)
            except Exception:
                continue
            rows.append({"image_path": str(target.relative_to(DATA_DIR.parents[0])), "label": class_dir.name})
    if not rows:
        return None
    manifest = DATA_DIR / "processed" / "driver_images.csv"
    pd.DataFrame(rows).to_csv(manifest, index=False)
    return manifest


def generate_all(seed: int = 42) -> dict[str, str]:
    return {
        "demand": str(prepare_cta_bus_ridership()),
        "recommendations": str(prepare_travel_recommendation_dataset() or generate_recommendations(seed)),
        "driver_images": str(prepare_driver_behavior_dataset() or generate_driver_images(seed)),
    }

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from .common import DATA_DIR, MODELS_DIR, OUTPUTS_DIR, ensure_dirs, write_json


def train_recommender(input_path: Path | None = None, k: int = 5) -> dict[str, float]:
    ensure_dirs()
    input_path = input_path or DATA_DIR / "processed" / "travel_interactions.csv"
    data = pd.read_csv(input_path)
    matrix = data.pivot_table(index="user_id", columns="destination", values="rating", fill_value=0)
    train_matrix = matrix.copy()
    held_out_by_user = {}
    rng = np.random.default_rng(42)
    for user in matrix.index:
        positives = list(matrix.columns[matrix.loc[user] >= 4])
        if len(positives) >= 2:
            held_out = rng.choice(positives)
            train_matrix.loc[user, held_out] = 0
            held_out_by_user[user] = held_out

    sim = cosine_similarity(train_matrix)
    users = list(matrix.index)
    destinations = list(matrix.columns)

    recommendations = {}
    hits = []
    recalls = []

    for idx, user in enumerate(users):
        held_out = held_out_by_user.get(user)
        if held_out is None:
            continue
        scores = sim[idx] @ train_matrix.values
        seen = set(train_matrix.columns[train_matrix.loc[user] > 0])
        ranked = [dest for _, dest in sorted(zip(scores, destinations), reverse=True) if dest not in seen][:k]
        recommendations[user] = ranked
        hits.append(int(held_out in ranked) / k)
        recalls.append(int(held_out in ranked))

    rec_rows = [{"user_id": user, "rank": i + 1, "destination": dest} for user, recs in recommendations.items() for i, dest in enumerate(recs)]
    pd.DataFrame(rec_rows).to_csv(OUTPUTS_DIR / "predictions" / "recommendations_sample.csv", index=False)
    metrics = {"precision_at_5": float(np.mean(hits) if hits else 0), "recall_at_5": float(np.mean(recalls) if recalls else 0)}
    write_json(OUTPUTS_DIR / "metrics" / "recommender_metrics.json", metrics)
    joblib.dump({"matrix": matrix, "similarity": sim, "recommendations": recommendations}, MODELS_DIR / "recommender_model.joblib")
    return metrics


def recommend_for_user(user_id: str, limit: int = 5) -> list[str]:
    model_path = MODELS_DIR / "recommender_model.joblib"
    if not model_path.exists():
        train_recommender()
    payload = joblib.load(model_path)
    return payload["recommendations"].get(user_id, [])[:limit]


def explain_recommendations(user_id: str, limit: int = 5) -> pd.DataFrame:
    model_path = MODELS_DIR / "recommender_model.joblib"
    if not model_path.exists():
        train_recommender()
    payload = joblib.load(model_path)
    matrix = payload["matrix"]
    similarity = payload["similarity"]
    users = list(matrix.index)
    if user_id not in users:
        return pd.DataFrame(columns=["rank", "destination", "reason"])

    user_index = users.index(user_id)
    neighbor_scores = sorted(
        [(score, other_user) for score, other_user in zip(similarity[user_index], users) if other_user != user_id],
        reverse=True,
    )
    best_neighbors = [other_user for _, other_user in neighbor_scores[:3]]
    rows = []
    for rank, destination in enumerate(recommend_for_user(user_id, limit=limit), start=1):
        supporters = [neighbor for neighbor in best_neighbors if matrix.loc[neighbor, destination] > 0]
        reason = "Destino frecuente en usuarios con historial similar"
        if supporters:
            reason = f"Recomendado por similitud con {', '.join(supporters[:2])}"
        rows.append({"rank": rank, "destination": destination, "reason": reason})
    return pd.DataFrame(rows)

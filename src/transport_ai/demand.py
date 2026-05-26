from __future__ import annotations

from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from .common import DATA_DIR, MODELS_DIR, OUTPUTS_DIR, ensure_dirs, write_json


FEATURES = ["dayofweek", "month", "is_weekend", "holiday", "lag_1", "lag_7", "rolling_7"]
TRAIN_START_DATE = "2021-01-01"
TOP_ROUTES = 10


def load_demand_dataset(input_path: Path | None = None) -> pd.DataFrame:
    input_path = input_path or DATA_DIR / "processed" / "cta_bus_ridership_daily_by_route.csv"
    raw = pd.read_csv(input_path)
    data = raw.rename(columns={"rides": "passengers"}).copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["passengers"] = pd.to_numeric(data["passengers"], errors="coerce")
    data = data.dropna(subset=["date", "route", "passengers"])
    data = data[data["date"] >= pd.Timestamp(TRAIN_START_DATE)]
    top_routes = data.groupby("route")["passengers"].sum().nlargest(TOP_ROUTES).index
    data = data[data["route"].isin(top_routes)].copy()
    if "daytype" in data.columns:
        data["holiday"] = data["daytype"].eq("U").astype(int)
    else:
        data["holiday"] = data["date"].dt.dayofweek.eq(6).astype(int)
    return data[["date", "route", "passengers", "holiday"]].sort_values(["route", "date"])


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data = data[["date", "route", "passengers", "holiday"]].copy()
    data["date"] = pd.to_datetime(data["date"])
    data = data.sort_values(["route", "date"])
    data["dayofweek"] = data["date"].dt.dayofweek
    data["month"] = data["date"].dt.month
    data["is_weekend"] = data["dayofweek"].isin([5, 6]).astype(int)
    for lag in [1, 7]:
        data[f"lag_{lag}"] = data.groupby("route")["passengers"].shift(lag)
    data["rolling_7"] = (
        data.groupby("route")["passengers"]
        .transform(lambda series: series.shift(1).rolling(7, min_periods=1).mean())
    )
    return data.dropna().reset_index(drop=True)


def train_demand_model(input_path: Path | None = None) -> dict[str, float]:
    ensure_dirs()
    raw = load_demand_dataset(input_path)
    metrics: dict[str, float] = {}
    predictions = []
    models = {}

    for route, route_df in build_features(raw).groupby("route"):
        route_df = route_df.sort_values("date")
        split = int(len(route_df) * 0.8)
        train = route_df.iloc[:split]
        test = route_df.iloc[split:]
        model = RandomForestRegressor(n_estimators=120, random_state=42, min_samples_leaf=2)
        model.fit(train[FEATURES], train["passengers"])
        pred = model.predict(test[FEATURES])
        mae = mean_absolute_error(test["passengers"], pred)
        rmse = float(np.sqrt(mean_squared_error(test["passengers"], pred)))
        mape = float(np.mean(np.abs((test["passengers"] - pred) / test["passengers"])) * 100)
        route_key = route.lower().replace(" ", "_")
        metrics[f"{route_key}_mae"] = float(mae)
        metrics[f"{route_key}_rmse"] = rmse
        metrics[f"{route_key}_mape"] = mape
        models[route] = model

        chart_df = test[["date", "route", "passengers"]].copy()
        chart_df["prediction"] = pred
        predictions.append(chart_df)

        plt.figure(figsize=(10, 4))
        plt.plot(test["date"], test["passengers"], label="Real")
        plt.plot(test["date"], pred, label="Prediccion")
        plt.title(f"Demanda real vs. predicha - {route}")
        plt.xticks(rotation=45, ha="right")
        plt.legend()
        plt.tight_layout()
        plt.savefig(OUTPUTS_DIR / "figures" / f"demand_{route_key}.png")
        plt.close()

    all_predictions = pd.concat(predictions, ignore_index=True)
    all_predictions.to_csv(OUTPUTS_DIR / "predictions" / "demand_predictions.csv", index=False)
    future_forecast = forecast_next_days(raw, models, days=30)
    future_forecast.to_csv(OUTPUTS_DIR / "predictions" / "demand_forecast_30_days.csv", index=False)
    write_json(OUTPUTS_DIR / "metrics" / "demand_metrics.json", metrics)
    joblib.dump({"features": FEATURES, "models": models}, MODELS_DIR / "demand_model.joblib")
    return metrics


def forecast_next_days(raw: pd.DataFrame, models: dict[str, RandomForestRegressor], days: int = 30) -> pd.DataFrame:
    rows = []
    data = raw.copy()
    data["date"] = pd.to_datetime(data["date"])

    for route, model in models.items():
        history = (
            data[data["route"] == route]
            .sort_values("date")[["date", "passengers"]]
            .copy()
            .reset_index(drop=True)
        )
        values = list(history["passengers"].astype(float))
        last_date = history["date"].max()

        for step in range(1, days + 1):
            date = last_date + pd.Timedelta(days=step)
            lag_1 = values[-1]
            lag_7 = values[-7] if len(values) >= 7 else values[-1]
            rolling_7 = float(np.mean(values[-7:]))
            features = pd.DataFrame(
                [
                    {
                        "dayofweek": date.dayofweek,
                        "month": date.month,
                        "is_weekend": int(date.dayofweek in [5, 6]),
                        "holiday": int(date.dayofweek in [6]),
                        "lag_1": lag_1,
                        "lag_7": lag_7,
                        "rolling_7": rolling_7,
                    }
                ],
                columns=FEATURES,
            )
            prediction = float(max(model.predict(features)[0], 0))
            values.append(prediction)
            rows.append(
                {
                    "date": date.date().isoformat(),
                    "route": route,
                    "forecast_passengers": round(prediction, 2),
                }
            )

    return pd.DataFrame(rows)

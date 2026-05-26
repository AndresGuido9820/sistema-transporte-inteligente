#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from transport_ai.sample_data import (
    prepare_cta_bus_ridership,
    prepare_driver_behavior_dataset,
    prepare_travel_recommendation_dataset,
)


if __name__ == "__main__":
    outputs = {
        "cta_bus_ridership": prepare_cta_bus_ridership(),
        "travel_recommendation_kaggle": prepare_travel_recommendation_dataset(),
        "driver_behavior_kaggle_sample": prepare_driver_behavior_dataset(),
    }
    for name, path in outputs.items():
        print(f"{name}: {path or 'no encontrado'}")

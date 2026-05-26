#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from transport_ai.demand import train_demand_model
from transport_ai.recommendation import train_recommender
from transport_ai.sample_data import generate_all
from transport_ai.vision import train_vision_model


def main() -> None:
    print("Preparando datasets...")
    print(generate_all())
    print("Entrenando predicción de demanda...")
    print(train_demand_model())
    print("Entrenando clasificación de imágenes...")
    print(train_vision_model())
    print("Entrenando recomendador...")
    print(train_recommender())


if __name__ == "__main__":
    main()

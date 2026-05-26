#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from transport_ai.vision import train_vision_model


if __name__ == "__main__":
    print(train_vision_model())

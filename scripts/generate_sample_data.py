#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from transport_ai.sample_data import generate_all


if __name__ == "__main__":
    for name, path in generate_all().items():
        print(f"{name}: {path}")

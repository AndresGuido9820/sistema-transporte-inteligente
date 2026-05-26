from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"
MODELS_DIR = ROOT / "models"


def ensure_dirs() -> None:
    for path in [
        DATA_DIR / "raw",
        DATA_DIR / "processed",
        OUTPUTS_DIR / "figures",
        OUTPUTS_DIR / "metrics",
        OUTPUTS_DIR / "predictions",
        MODELS_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


import os
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
SCRIPTS_DIR = ROOT / "scripts"
APP_DIR = ROOT / "app"


def require_file(relative_path: str) -> Path:
    path = ROOT / relative_path
    if not path.exists():
        pytest.skip(f"Falta {relative_path}; se espera crear este modulo para habilitar la prueba.")
    return path


def run_python_script(script_path: Path, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{SRC}{os.pathsep}{ROOT}{os.pathsep}{env.get('PYTHONPATH', '')}"
    env["TRANSPORTE_DATA_DIR"] = str(tmp_path / "data")
    env["TRANSPORTE_OUTPUT_DIR"] = str(tmp_path / "outputs")
    env["TRANSPORTE_MODEL_DIR"] = str(tmp_path / "models")

    return subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=90,
        check=False,
    )


def assert_script_succeeds(script_path: Path, tmp_path: Path) -> None:
    result = run_python_script(script_path, tmp_path)
    assert result.returncode == 0, (
        f"{script_path.relative_to(ROOT)} fallo con codigo {result.returncode}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )


def test_generate_sample_data_script_can_run(tmp_path: Path) -> None:
    script = require_file("scripts/generate_sample_data.py")

    assert_script_succeeds(script, tmp_path)


@pytest.mark.parametrize(
    "relative_path",
    [
        "scripts/train_demand.py",
        "scripts/train_recommender.py",
    ],
)
def test_training_scripts_can_run(relative_path: str, tmp_path: Path) -> None:
    script = require_file(relative_path)
    generator = SCRIPTS_DIR / "generate_sample_data.py"
    if generator.exists():
        assert_script_succeeds(generator, tmp_path)

    assert_script_succeeds(script, tmp_path)


def test_demand_training_generates_30_day_forecast(tmp_path: Path) -> None:
    generator = require_file("scripts/generate_sample_data.py")
    trainer = require_file("scripts/train_demand.py")

    assert_script_succeeds(generator, tmp_path)
    assert_script_succeeds(trainer, tmp_path)

    forecast_path = ROOT / "outputs" / "predictions" / "demand_forecast_30_days.csv"
    assert forecast_path.exists()
    forecast = forecast_path.read_text(encoding="utf-8")
    assert "forecast_passengers" in forecast


def test_streamlit_app_imports() -> None:
    app_file = require_file("app/streamlit_app.py")
    pytest.importorskip("streamlit")

    result = subprocess.run(
        [sys.executable, "-c", f"import runpy; runpy.run_path({str(app_file)!r}, run_name='__test__')"],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": f"{SRC}{os.pathsep}{ROOT}{os.pathsep}{os.environ.get('PYTHONPATH', '')}"},
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )

    assert result.returncode == 0, (
        f"No se pudo importar {app_file.relative_to(ROOT)}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )


def test_notebooks_are_valid_json() -> None:
    notebooks = [
        "notebooks/01_prediccion_demanda.ipynb",
        "notebooks/02_clasificacion_conduccion.ipynb",
        "notebooks/03_recomendacion_destinos.ipynb",
    ]
    for relative_path in notebooks:
        notebook = require_file(relative_path)
        payload = json.loads(notebook.read_text(encoding="utf-8"))
        assert payload["nbformat"] == 4
        assert payload["cells"], f"{relative_path} no tiene celdas"
        full_text = "\n".join("".join(cell.get("source", "")) for cell in payload["cells"])
        assert ("git " + "clone") not in full_text.lower()
        assert "Herramienta" in full_text


def test_pages_are_split_between_tools_and_report() -> None:
    index = require_file("docs/index.html").read_text(encoding="utf-8")
    report = require_file("docs/reporte.html").read_text(encoding="utf-8")

    assert "Herramientas ejecutables en Google Colab" in index
    assert "Reporte Técnico" in report

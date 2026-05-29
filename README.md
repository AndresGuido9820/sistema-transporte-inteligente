# Sistema Inteligente Integrado para Transporte

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![TF.js](https://img.shields.io/badge/TensorFlow.js-GraphModel-orange?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/js)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-brightgreen?logo=github&logoColor=white)](https://andresguido9820.github.io/sistema-transporte-inteligente/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Curso:** Aplicaciones en sistemas de recomendación e imágenes · **Profesor:** Juan David Ospina Arango  
**Universidad Nacional de Colombia** · 2026  
**Autores:** Andrés F. Guido Montoya · Juan José Martínez · Andrés Lemus

[Herramientas web](https://andresguido9820.github.io/sistema-transporte-inteligente/) · [Reporte técnico](https://andresguido9820.github.io/sistema-transporte-inteligente/reporte.html) · [Reporte fuente](report/blog_post.md)

</div>

---

## Resumen

Proyecto académico que integra tres soluciones para una empresa de transporte:

| Módulo | Objetivo | Métricas |
|---|---|---|
| Predicción de demanda | Estimar pasajeros por ruta para los próximos 30 días | MAE, RMSE, MAPE |
| Clasificación de conducción distractiva | Detectar comportamientos de riesgo desde imágenes | Accuracy, precision, recall, F1 |
| Recomendación de destinos | Sugerir destinos personalizados por usuario | Precision@K, Recall@K |

El repositorio incluye datos procesados reproducibles en `data/processed/` para que los Colabs corran sin credenciales externas. La procedencia de cada archivo está documentada en [data/README.md](data/README.md). La demanda de transporte usa datos reales diarios por ruta de Chicago Transit Authority, y los módulos de imágenes y recomendación usan datasets de Kaggle. Si los datasets reales están descargados en `data/raw/`, `scripts/prepare_real_datasets.py` crea muestras livianas para entrenamiento local sin versionar archivos grandes.

---

## Ejecución Local

Los notebooks corren en Google Colab (links en la tabla de abajo). La herramienta web corre en el navegador sin instalación:

```
https://andresguido9820.github.io/sistema-transporte-inteligente/
```

Para reproducir localmente con Python:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/prepare_real_datasets.py
```

---

## Estructura

```txt
sistema-transporte-inteligente/
├── data/                      # Datos raw y processed
├── docs/                      # Herramienta web (GitHub Pages)
│   ├── index.html             #   Portal principal
│   ├── notebook01.html        #   Módulo predicción (Pyodide)
│   ├── notebook02.html        #   Módulo clasificación (TF.js)
│   ├── notebook03.html        #   Módulo recomendación
│   ├── reporte.html           #   Reporte técnico
│   └── model/                 #   CNN MobileNetV2 (TF.js GraphModel)
├── notebooks/                 # Colabs de entrenamiento
├── outputs/                   # Métricas, figuras y predicciones
├── report/                    # Reporte tipo blog y teoría por módulo
├── scripts/                   # Scripts de preparación de datos
└── tests/                     # Pruebas automatizadas
```

---

## Documentación

| Archivo | Descripción |
|---|---|
| [blog_post.md](report/blog_post.md) | Reporte principal tipo blog |
| [teoria_01_prediccion_demanda.md](report/teoria_01_prediccion_demanda.md) | Marco teórico de series de tiempo |
| [teoria_02_clasificacion_imagenes.md](report/teoria_02_clasificacion_imagenes.md) | Marco teórico de clasificación visual |
| [teoria_03_recomendacion_destinos.md](report/teoria_03_recomendacion_destinos.md) | Marco teórico de recomendación |
| [casos_de_uso.md](report/casos_de_uso.md) | Casos de uso |
| [discusion.md](report/discusion.md) | Limitaciones y trabajo futuro |
| [aspectos_eticos.md](report/aspectos_eticos.md) | Privacidad, sesgos y uso responsable |
| [datasets_reales.md](docs/datasets_reales.md) | Fuentes y preparación de datasets reales |

---

## Herramientas en Colab

Cada notebook está organizado como una herramienta independiente: carga datos, entrena/evalúa el modelo y termina con una celda de uso con parámetros editables.

| # | Herramienta | Salidas principales | Colab |
|---|---|---|
| 01 | Predicción de demanda | Métricas por ruta, gráficas real vs. predicción y pronóstico de 30 días | [Abrir](https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/01_prediccion_demanda.ipynb) |
| 02 | Clasificación de conducción | Matriz de confusión, reporte por clase y clasificador de imagen nueva | [Abrir](https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/02_clasificacion_conduccion.ipynb) |
| 03 | Recomendación de destinos | Precision@K, Recall@K y recomendaciones explicadas por usuario | [Abrir](https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/03_recomendacion_destinos.ipynb) |

---

## Resultados Actuales

| Módulo | Resultado |
|---|---|
| Demanda | MAE promedio 1096.71, RMSE promedio 1452.42, MAPE promedio 8.24% |
| Visión | MobileNetV2 fine-tuned — accuracy ~0.87, macro F1 ~0.86 (ver Colab para métricas exactas) |
| Recomendación | Precision@5 0.20, Recall@5 1.00 |

Las salidas reproducibles están en `outputs/metrics/`, `outputs/figures/`, `outputs/predictions/` y `outputs/screenshots/`.

---

## Datasets Recomendados

- Chicago Data Portal. CTA - Ridership - Bus Routes - Daily Totals by Route. https://data.cityofchicago.org/Transportation/CTA-Ridership-Bus-Routes-Daily-Totals-by-Route/jyb9-n7fm
- Kaggle. Multi-Class Driver Behavior Image Dataset.
- Kaggle. Travel Recommendation Dataset.

## Datos Usados

| Módulo | Archivo usado en Colab | Fuente documentada |
|---|---|---|
| Demanda | `data/processed/cta_bus_ridership_daily_by_route.csv` | Chicago Transit Authority, demanda diaria por ruta de bus |
| Conducción | `data/processed/driver_images.csv` | Kaggle Multi-Class Driver Behavior Image Dataset |
| Recomendación | `data/processed/travel_interactions.csv` | Kaggle Travel Recommendation Dataset |

---

## Citar

```bibtex
@misc{guido2026transporte,
  author = {Guido Montoya, Andres Felipe and Martinez, Juan Jose and Lemus, Andres},
  title = {Sistema Inteligente Integrado para Transporte},
  year = {2026},
  url = {https://github.com/AndresGuido9820/sistema-transporte-inteligente}
}
```

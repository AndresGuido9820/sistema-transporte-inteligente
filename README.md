# Sistema Inteligente Integrado para Transporte

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![TF.js](https://img.shields.io/badge/TensorFlow.js-GraphModel-orange?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/js)
[![GitHub Pages](https://img.shields.io/badge/Demo-live-brightgreen?logo=github&logoColor=white)](https://andresguido9820.github.io/sistema-transporte-inteligente/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Curso:** Aplicaciones en sistemas de recomendación e imágenes  
**Profesor:** Juan David Ospina Arango  
**Universidad Nacional de Colombia · 2026**  
**Autores:** Andrés F. Guido Montoya · Juan José Martínez · Andrés Lemus

---

[🌐 Herramientas web](https://andresguido9820.github.io/sistema-transporte-inteligente/) &nbsp;·&nbsp;
[📄 Reporte técnico](https://andresguido9820.github.io/sistema-transporte-inteligente/reporte.html) &nbsp;·&nbsp;
[▶️ Demo en video](https://www.youtube.com/watch?v=iRVR9MBd5Jg)

</div>

---

## Descripción general

Proyecto académico que diseña, entrena y despliega tres módulos de aprendizaje automático orientados a problemas operativos reales de una empresa de transporte. Cada módulo es independiente, entrena sobre datos reales y se publica como herramienta ejecutable en Google Colab y como demo web en GitHub Pages — sin servidor, sin instalación.

| Módulo | Problema | Modelo | Resultado |
|--------|----------|--------|-----------|
| **M1 — Predicción de demanda** | Pronosticar pasajeros por ruta a 30 días | LSTM multivariado (3 canales, ventana 14 días) | MAPE media **19.62%**, mín 8.69% (ruta 22) |
| **M2 — Clasificación de conducción** | Detectar comportamiento distractivo en conductores | MobileNetV2 fine-tuned → TF.js GraphModel | Accuracy **~0.87**, +19 pp vs baseline HOG+GB |
| **M3 — Recomendación de destinos** | Sugerir destinos personalizados por usuario | CF + CB Híbrido (0.7/0.3) | Hit Rate **79%**, NDCG@5 0.699 |

---

## Demo en vivo

La herramienta web corre completamente en el navegador — sin servidor, sin instalar nada:

```
https://andresguido9820.github.io/sistema-transporte-inteligente/
```

- **Módulo 01:** resultados pre-computados con pronóstico a 30 días por ruta
- **Módulo 02:** clasifica una imagen de conductor en tiempo real vía TF.js (~220 ms)
- **Módulo 03:** búsqueda instantánea de recomendaciones para cualquier usuario del dataset

---

## Módulos en detalle

### M1 — Predicción de demanda (LSTM multivariado)

**Dataset:** CTA – Bus Routes Daily Totals (Chicago Data Portal, 2021–2026). 10 rutas de mayor demanda, ~1 800 registros por ruta.

**Arquitectura:**
```
Input(14, 3) → LSTM(64, return_sequences=True) → LSTM(32) → Dense(16, relu) → Dense(1)
```

Los 3 canales de entrada son: (1) pasajeros normalizados por MinMaxScaler, (2) flag festivo/domingo (`daytype='U'`), (3) día de semana normalizado a [0,1]. Los canales 2 y 3 son deterministas — se calculan desde la fecha sin error acumulado.

**Resultados por ruta:**

| Ruta | MAE | MAPE | Nota |
|------|-----|------|------|
| 22 | 1 842 | **8.69%** | Más estable |
| 49 | 2 491 | 17.04% | Mayor mejora con canal festivo (−10.6 pp) |
| 8  | 3 420 | **25.62%** | Mayor variabilidad (CV=0.31) |
| Media | 2 676 | **19.62%** | −4.4 pp vs LSTM univariado |

**Colab:** [01_prediccion_demanda.ipynb](https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/01_prediccion_demanda.ipynb)

---

### M2 — Clasificación de conducción distractiva (MobileNetV2)

**Dataset:** Multi-Class Driver Behavior Image Dataset (Afridi, 2024; DOI: [10.17632/mzb4b6dff3.1](https://doi.org/10.17632/mzb4b6dff3.1)). 7 276 imágenes, 5 clases: `safe_driving`, `texting_phone`, `talking_phone`, `turning`, `other_activities`.

**Pipeline:**
- Redimensión a 96×96, normalización a [−1, 1]
- Data augmentation: flip horizontal, variación de brillo/contraste/saturación
- Partición estratificada 70/15/15 (seed=42)

**Entrenamiento en dos fases:**
1. Base MobileNetV2 congelada, solo cabeza: `GAP → Dense(256) → Dropout(0.4) → Dense(128) → Dropout(0.3) → Softmax(5)`, Adam lr=1e-3
2. Fine-tuning últimas 30 capas de MobileNetV2, Adam lr=1e-4

**Comparativa:**

| Modelo | Accuracy | F1 Macro |
|--------|----------|----------|
| HOG + Gradient Boosting (baseline) | 0.68 | 0.67 |
| MobileNetV2 solo cabeza | 0.81 | 0.79 |
| **MobileNetV2 fine-tuned** | **~0.87** | **0.85** |

El modelo exportado en TF.js GraphModel (`docs/model/`) corre inferencia directamente en el navegador a ~220 ms por imagen.

**Colab:** [02_clasificacion_conduccion.ipynb](https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/02_clasificacion_conduccion.ipynb)

---

### M3 — Recomendación de destinos (CF + CB híbrido)

**Dataset:** Travel Recommendation Dataset (Mehra, 2024, MIT). 858 usuarios, 866 destinos, 1 998 interacciones únicas (sparsity 99.73%).

**Sistema híbrido:**
- **CF:** similitud coseno user-user sobre matriz de ratings → `score_CF(u,i) = Σ sim(u,v)·r(v,i)`
- **CB:** match de preferencias declaradas al tipo de destino + bonus de popularidad
- **Híbrido:** `0.7 × CF + 0.3 × CB`

**Evaluación Leave-One-Out (181 usuarios, K=5):**

| Modo | Precision@5 | Recall@5 (Hit Rate) | NDCG@5 |
|------|-------------|---------------------|--------|
| CF | 0.158 | **0.790** | 0.699 |
| Híbrido 0.7/0.3 | 0.141 | 0.707 | 0.626 |
| CB puro | 0.001 | 0.006 | 0.004 |

Cobertura de catálogo: 72% (624 de 866 destinos aparecen en al menos un Top-5).

**Colab:** [03_recomendacion_destinos.ipynb](https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/03_recomendacion_destinos.ipynb)

---

## Herramienta web — arquitectura sin servidor

Toda la lógica corre en el navegador del usuario:

- **Módulo 01:** resultados pre-computados embebidos como imágenes (sin ejecución en tiempo real)
- **Módulo 02:** TensorFlow.js 4.17 — carga `docs/model/model.json` + shards (~10 MB), inferencia vía WebGL
- **Módulo 03:** Pyodide 0.25 (Python/WASM) — carga JSONs pre-computados, búsqueda y filtrado en Python puro

Ventajas: cero costos de backend, privacidad (los datos no salen del dispositivo), disponibilidad garantizada en GitHub Pages.

---

## Estructura del repositorio

```
sistema-transporte-inteligente/
├── data/
│   ├── processed/             # CSVs y JSONs listos para Colab
│   │   ├── cta_bus_ridership_daily_by_route.csv
│   │   ├── driver_images.csv
│   │   ├── travel_interactions.csv
│   │   ├── users.csv · destinations.csv · reviews.csv · user_history.csv
│   │   └── recommendations.json  # Top-5 por usuario (858 entradas)
│   └── README.md              # Procedencia de cada dataset
├── docs/                      # Herramienta web — GitHub Pages
│   ├── index.html             # Portal principal con los 3 módulos
│   ├── notebook01.html        # Demo predicción (resultados pre-computados)
│   ├── notebook02.html        # Demo clasificación (TF.js en vivo)
│   ├── notebook03.html        # Demo recomendación (Pyodide + JSON)
│   ├── reporte.html           # Reporte técnico completo (808 líneas)
│   ├── model/                 # MobileNetV2 TF.js GraphModel (~10 MB)
│   └── assets/                # Imágenes para la web
├── notebooks/                 # Notebooks de entrenamiento (Colab)
│   ├── 01_prediccion_demanda.ipynb
│   ├── 02_clasificacion_conduccion.ipynb
│   └── 03_recomendacion_destinos.ipynb
├── outputs/
│   ├── figures/               # Gráficas de demanda y matriz de confusión
│   ├── metrics/               # demand_metrics.json · vision_metrics.json · recommender_metrics.json
│   └── predictions/           # Predicciones y pronósticos CSV
├── report/                    # Documentos teóricos por módulo
├── scripts/                   # Scripts de preparación de datos y entrenamiento
├── src/transport_ai/          # Módulos Python reutilizables
├── tests/                     # Pruebas automatizadas (pytest)
├── .github/workflows/         # validacion.yml — CI con pytest en cada push
├── requirements.txt
└── pyproject.toml
```

---

## Ejecución local

Los notebooks están diseñados para Google Colab (T4 GPU para M2). Para ejecutar localmente:

```bash
git clone https://github.com/AndresGuido9820/sistema-transporte-inteligente.git
cd sistema-transporte-inteligente
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Los datos en `data/processed/` están listos para usar directamente. Las imágenes de conducción (`driver_images_real/`) no se versionan en git por su tamaño (2.4 GB); se obtienen desde el dataset original en Mendeley Data (DOI: 10.17632/mzb4b6dff3.1).

Para regenerar los datos procesados desde las fuentes originales:

```bash
python scripts/prepare_real_datasets.py
```

Para ejecutar las pruebas:

```bash
pytest -q
```

---

## Datasets

| Módulo | Fuente | Acceso |
|--------|--------|--------|
| M1 — Demanda | CTA Bus Routes Daily Totals · Chicago Data Portal | [data.cityofchicago.org](https://data.cityofchicago.org/Transportation/CTA-Ridership-Bus-Routes-Daily-Totals-by-Route/jyb9-n7fm) |
| M2 — Conducción | Multi-Class Driver Behavior Image Dataset · Mendeley Data | [doi.org/10.17632/mzb4b6dff3.1](https://doi.org/10.17632/mzb4b6dff3.1) |
| M3 — Recomendación | Travel Recommendation Dataset · Kaggle | [kaggle.com/datasets/amanmehra23](https://www.kaggle.com/datasets/amanmehra23/travel-recommendation-dataset) |

---

## CI/CD

Cada push a cualquier rama ejecuta el workflow `.github/workflows/validacion.yml`:
- Checkout con sparse-checkout (solo archivos necesarios, sin imágenes)
- Setup Python 3.11
- `pip install` de dependencias de prueba
- `pytest -q` sobre `tests/test_flujos_principales.py`

El deploy a GitHub Pages se realiza manualmente pusheando a la rama `gh-pages`.

---

## Citar

```bibtex
@misc{guido2026transporte,
  author  = {Guido Montoya, Andres Felipe and Martinez, Juan Jose and Lemus, Andres},
  title   = {Sistema Inteligente Integrado para Transporte},
  year    = {2026},
  url     = {https://github.com/AndresGuido9820/sistema-transporte-inteligente}
}
```

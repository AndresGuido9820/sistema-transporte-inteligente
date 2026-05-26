# Datos

Esta carpeta separa los datos originales no versionados y los archivos procesados livianos que usa la entrega.

## Fuentes

| Archivo procesado | Módulo | Fuente base | Descripción |
|---|---|---|---|
| `data/processed/cta_bus_ridership_daily_by_route.csv` | Predicción de demanda | Chicago Data Portal / Chicago Transit Authority: CTA Ridership - Bus Routes - Daily Totals by Route | Dataset completo de demanda diaria por ruta, con registros desde 2001 hasta 2026. El Colab filtra desde 2021 y selecciona las rutas con mayor demanda reciente. |
| `data/processed/driver_images.csv` y `data/processed/driver_images_real/` | Clasificación de conducción | Kaggle: Multi-Class Driver Behavior Image Dataset | Muestra liviana con rutas de imagen y etiqueta de comportamiento. |
| `data/processed/travel_interactions.csv` | Recomendación de destinos | Kaggle: Travel Recommendation Dataset | Interacciones usuario-destino normalizadas para filtrado colaborativo. |

## `raw/`

Aquí van los datasets originales descargados localmente. No se versionan por tamaño.

Descarga y preparación recomendada:

```bash
kaggle datasets download -d arafatsahinafridi/multi-class-driver-behavior-image-dataset -p data/raw/driver_behavior --unzip
kaggle datasets download -d amanmehra23/travel-recommendation-dataset -p data/raw/travel_recommendation --unzip
python scripts/prepare_real_datasets.py
```

El dataset de demanda se obtiene desde Chicago Data Portal:

```text
https://data.cityofchicago.org/Transportation/CTA-Ridership-Bus-Routes-Daily-Totals-by-Route/jyb9-n7fm
```

## `processed/`

Aquí van los archivos listos para notebooks, app y pruebas. Se versionan porque son pequeños y permiten reproducir la entrega en Colab sin descargar archivos pesados.

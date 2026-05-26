# Datasets reales usados

## Predicción de demanda

Dataset: CTA - Ridership - Bus Routes - Daily Totals by Route.

Fuente: Chicago Data Portal / Chicago Transit Authority.

El archivo usado contiene demanda diaria real por ruta de bus en Chicago. Se conserva completo en `data/processed/cta_bus_ridership_daily_by_route.csv`, con datos desde 2001 hasta 2026. Para entrenar el modelo de forma rápida y operativa, el notebook filtra desde 2021 y selecciona las rutas con mayor demanda reciente.

Columnas principales:

- `route`: código de ruta.
- `date`: fecha diaria.
- `daytype`: tipo de día (`W` laboral, `A` sábado, `U` domingo/festivo).
- `rides`: pasajeros diarios de la ruta.

URL: https://data.cityofchicago.org/Transportation/CTA-Ridership-Bus-Routes-Daily-Totals-by-Route/jyb9-n7fm

## Clasificación de conducción distractiva

Dataset: Multi-Class Driver Behavior Image Dataset.

Descarga:

```bash
kaggle datasets download -d arafatsahinafridi/multi-class-driver-behavior-image-dataset -p data/raw/driver_behavior --unzip
```

El dataset completo pesa aproximadamente 2.4 GB. Para mantener el repo liviano, se genera una muestra redimensionada en `data/processed/driver_images_real/`.

URL: https://www.kaggle.com/datasets/arafatsahinafridi/multi-class-driver-behavior-image-dataset

## Recomendación de destinos

Dataset: Travel Recommendation Dataset.

Descarga:

```bash
kaggle datasets download -d amanmehra23/travel-recommendation-dataset -p data/raw/travel_recommendation --unzip
```

Archivos usados:

- `Expanded_Destinations.csv`
- `Final_Updated_Expanded_UserHistory.csv`
- `Final_Updated_Expanded_Users.csv`
- `Final_Updated_Expanded_Reviews.csv`

El preprocesamiento une historial de usuario con metadatos de destino para crear `data/processed/travel_interactions.csv`.

URL: https://www.kaggle.com/datasets/amanmehra23/travel-recommendation-dataset

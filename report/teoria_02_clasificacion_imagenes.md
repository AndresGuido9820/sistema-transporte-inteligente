# Teoría — Clasificación de Conducción Distractiva

## 1. Problema

La conducción distractiva es un factor de riesgo para pasajeros, peatones y otros actores viales. Este módulo busca clasificar imágenes de conductores en categorías de comportamiento, por ejemplo conducción normal, uso del teléfono móvil, somnolencia o distracción visual.

## 2. Dataset

El dataset recomendado es *Multi-Class Driver Behavior Image Dataset* de Kaggle. Contiene imágenes etiquetadas con varias clases de comportamiento del conductor. Para desarrollo local se dejará un modo demo que permita probar el pipeline aunque el dataset completo no esté descargado.

## 3. Preprocesamiento

El preprocesamiento incluirá:

- Redimensionamiento de imágenes.
- Normalización.
- División entrenamiento, validación y prueba.
- Aumentación de datos: recortes, rotaciones suaves, cambios de brillo y contraste.

## 4. Modelo

El modelo principal será una red convolucional con transferencia de aprendizaje. La opción inicial será ResNet18 con PyTorch, reemplazando la última capa por una capa compatible con el número de clases.

La transferencia de aprendizaje reduce el costo de entrenamiento y mejora el desempeño cuando el dataset disponible no es muy grande.

## 5. Métricas

Las métricas serán:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Matriz de confusión.

El F1-score es especialmente importante si las clases están desbalanceadas.

## 6. Entregables

- Modelo entrenado.
- Métricas de evaluación.
- Matriz de confusión.
- Ejemplos de clasificaciones correctas.
- Casos erróneos y análisis de posibles causas.
- Medidas preventivas recomendadas.


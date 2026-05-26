# Sistema Inteligente Integrado para Predicción, Clasificación y Recomendación en una Empresa de Transporte

**Curso:** Aplicaciones en sistemas de recomendación e imágenes  
**Profesor:** Juan David Ospina Arango  
**Universidad:** Universidad Nacional de Colombia  
**Autores:** Andrés F. Guido Montoya, Juan José Martínez, Andrés Lemus  
**Fecha:** Mayo de 2026  
**Repositorio:** https://github.com/AndresGuido9820/sistema-transporte-inteligente

---

## Resumen Ejecutivo

Este proyecto propone un sistema inteligente para una empresa de transporte que integra tres capacidades de aprendizaje profundo y aprendizaje automático: predicción de demanda por ruta, clasificación de comportamientos distractivos en conductores a partir de imágenes y recomendación personalizada de destinos. La solución busca mejorar la asignación de vehículos y personal, fortalecer la seguridad vial y aumentar la relevancia de las sugerencias de viaje para los usuarios.

El sistema se implementó en Python, con módulos independientes para datos, modelos, evaluación y visualización. Además de la demo web, se construyeron tres herramientas en Google Colab: una para pronóstico de demanda, una para clasificación de imágenes y una para recomendación personalizada de destinos. El reporte técnico se publica aparte en GitHub Pages para separar la documentación de las herramientas ejecutables.

---

## 1. Introducción

Las empresas de transporte operan bajo incertidumbre diaria: la demanda cambia por ruta, temporada, día de la semana, eventos externos y comportamiento de los usuarios. Al mismo tiempo, la seguridad del servicio depende de detectar prácticas de conducción riesgosa, como uso del celular, somnolencia o distracción visual. Finalmente, la experiencia del cliente puede mejorar si la plataforma sugiere destinos coherentes con su historial y preferencias.

El objetivo general es desarrollar una solución integrada que combine modelos predictivos, clasificación visual y sistemas de recomendación. El alcance académico incluye entrenamiento, evaluación, documentación técnica, análisis ético y una demo web funcional.

---

## 2. Metodología

El proyecto se organizó en cuatro fases:

1. Preparación de datos: limpieza, transformación, partición de entrenamiento/prueba y generación de muestras procesadas livianas a partir de los datasets reales.
2. Modelado: entrenamiento independiente de los tres módulos usando modelos base y modelos principales.
3. Evaluación: cálculo de métricas específicas para cada problema y generación de gráficas.
4. Integración: construcción de una herramienta web para visualizar resultados y probar los modelos.

La arquitectura sigue una separación por módulos para facilitar la reproducibilidad: `src/transport_ai/demand.py`, `src/transport_ai/vision.py` y `src/transport_ai/recommendation.py`.

### 2.1 Ideación y Canvas

La propuesta se diseñó a partir de un enfoque Canvas orientado a una empresa de transporte:

| Elemento | Definición |
|---|---|
| Usuarios principales | Planeadores de operación, equipo de seguridad vial y clientes de la plataforma |
| Problemas clave | Demanda variable, riesgo por distracción del conductor y baja personalización de destinos |
| Propuesta de valor | Reducir incertidumbre operativa, apoyar prevención de incidentes y mejorar experiencia del usuario |
| Datos necesarios | Historial de rutas, imágenes etiquetadas de conducción e interacciones usuario-destino |
| Métricas de éxito | Menor error de pronóstico, mayor F1 visual y mejor Recall@K en recomendaciones |
| Riesgos | Sesgos de datos, privacidad de imágenes, sobreajuste y baja cobertura de usuarios nuevos |

### 2.2 Plan de Calidad

La calidad se validó con tres niveles: pruebas automatizadas, ejecución completa de scripts y revisión manual de salidas. Las pruebas verifican generación de datos, entrenamiento de modelos, notebooks válidos y carga de la app. La ejecución completa produce métricas, figuras, predicciones y modelos serializados.

---

## 3. Desarrollo Técnico por Módulo

### 3.1 Predicción de Demanda de Transporte

El primer módulo predice la demanda diaria por rutas específicas de bus. Para este módulo se usa el dataset *CTA - Ridership - Bus Routes - Daily Totals by Route*, publicado por Chicago Transit Authority en Chicago Data Portal.

El archivo se conserva completo en el repositorio con datos desde 2001 hasta 2026. Para el entrenamiento se filtra desde 2021 y se seleccionan las 10 rutas con mayor demanda reciente. La variable `rides` se usa como `passengers`, y `daytype` permite diferenciar días laborales, sábados y domingos/festivos.

El modelo implementado es un `RandomForestRegressor` con variables temporales, rezagos y medias móviles. Las métricas promedio obtenidas sobre las rutas seleccionadas fueron MAE 1096.71, RMSE 1452.42 y MAPE 8.24%; el error absoluto se interpreta como pasajeros diarios por ruta.

Como salida operativa adicional, el módulo genera `outputs/predictions/demand_forecast_30_days.csv`, con una estimación diaria para los próximos 30 días por ruta. Esta tabla es la base para decisiones de asignación de vehículos, turnos de conductores y refuerzo de rutas con mayor demanda esperada.

### 3.2 Clasificación de Conducción Distractiva

El segundo módulo clasifica imágenes de conductores en categorías del dataset Multi-Class Driver Behavior Image Dataset de Kaggle: `safe_driving`, `talking_phone`, `texting_phone`, `turning` y `other_activities`.

Para mantener ejecución rápida en Colab y CI se entrenó un clasificador liviano sobre una muestra real redimensionada. Las métricas fueron accuracy 0.46, macro precision 0.459, macro recall 0.460 y macro F1 0.448. La herramienta muestra también las probabilidades por clase para identificar casos ambiguos. Como mejora futura queda reemplazarlo por transferencia de aprendizaje con ResNet18, MobileNet o EfficientNet.

### 3.3 Sistema de Recomendación de Destinos

El tercer módulo recomienda destinos de viaje a usuarios según historial, preferencias y comportamiento de reserva. Se usó Travel Recommendation Dataset de Kaggle, uniendo historial de usuario con metadatos de destinos.

El enfoque implementado es filtrado colaborativo con similitud coseno usuario-usuario. Las métricas fueron Precision@5 = 0.20 y Recall@5 = 1.00 en la evaluación leave-one-out implementada. Además, la herramienta entrega explicaciones simples de las recomendaciones, basadas en usuarios con historial similar.

---

## 4. Herramienta Web

La demo web se construyó con Streamlit. Tiene tres vistas principales:

- Predicción de demanda: selección de ruta, gráfica histórica y predicción a 30 días.
- Clasificación de conducción: carga de imagen, clase predicha y confianza.
- Recomendación de destinos: selección de usuario y lista de destinos sugeridos.

La interfaz se enfocó en una experiencia operativa, clara y fácil de demostrar en video.

Además, se publicaron páginas estáticas en GitHub Pages:

- Portada de herramientas: https://andresguido9820.github.io/sistema-transporte-inteligente/
- Reporte técnico: https://andresguido9820.github.io/sistema-transporte-inteligente/reporte.html
- Herramientas Colab: enlaces directos a los tres notebooks desde la portada.

Capturas generadas:

- `outputs/screenshots/app_demanda.png`
- `outputs/screenshots/app_mobile.png`

---

## 5. Resultados Generales y Discusión

Los tres módulos se ejecutan de extremo a extremo mediante `python scripts/run_all.py`. Las pruebas automatizadas validan generación de datos, entrenamiento, importación de la app y estructura de notebooks.

| Módulo | Resultado principal | Archivo |
|---|---:|---|
| Demanda | MAE promedio 1096.71, RMSE promedio 1452.42, MAPE promedio 8.24% | `outputs/metrics/demand_metrics.json` |
| Visión | Accuracy 0.46, macro F1 0.448 | `outputs/metrics/vision_metrics.json` |
| Recomendación | Precision@5 0.20, Recall@5 1.00 | `outputs/metrics/recommender_metrics.json` |

La clasificación visual muestra el principal punto débil: el modelo liviano no reemplaza una CNN profunda. Sin embargo, el pipeline completo de datos reales, entrenamiento, evaluación y demo web ya está listo para sustituir el clasificador por una arquitectura de transferencia.

### 5.1 Evidencias Reproducibles

| Evidencia | Ubicación |
|---|---|
| Predicciones históricas de demanda | `outputs/predictions/demand_predictions.csv` |
| Pronóstico de 30 días | `outputs/predictions/demand_forecast_30_days.csv` |
| Recomendaciones de muestra | `outputs/predictions/recommendations_sample.csv` |
| Métricas por módulo | `outputs/metrics/` |
| Gráficas generadas | `outputs/figures/` |
| Capturas de la herramienta web | `outputs/screenshots/` |

### 5.2 Pruebas de Funcionamiento

El flujo se valida con `pytest`, que ejecuta pruebas sobre datos, entrenamiento, estructura de notebooks e importación de la app. También se configuró GitHub Actions para ejecutar la validación en cada actualización de `main`.

---

## 6. Aspectos Éticos y Creatividad

El uso de imágenes de conductores requiere manejo responsable de datos personales, consentimiento, anonimización y control de acceso. El sistema no debe utilizarse como mecanismo automático de sanción sin revisión humana. En recomendación, deben evitarse sesgos que limiten la diversidad de destinos o refuercen patrones históricos injustos.

La creatividad del proyecto está en integrar tres capacidades distintas en una sola herramienta de operación para transporte: planificación, seguridad y experiencia de usuario.

---

## 7. Conclusiones y Recomendaciones

El sistema propuesto permite abordar problemas reales de una empresa de transporte desde una perspectiva integrada. La predicción de demanda ayuda a planificar recursos, la clasificación de imágenes apoya la seguridad vial y la recomendación de destinos mejora la personalización del servicio.

Como trabajo futuro se recomienda incorporar clima real, eventos de ciudad, más rutas, datos reales anonimizados de usuarios y validación con usuarios finales.

### 7.1 Contribuciones del Equipo

| Integrante | Contribución principal |
|---|---|
| Andrés F. Guido Montoya | Integración del repositorio, demo web, automatización y reporte |
| Juan José Martínez | Módulo de demanda, análisis de series de tiempo y visualizaciones |
| Andrés Lemus | Módulo de imágenes, recomendación y revisión de resultados |

## 8. Anexos

- Repositorio: https://github.com/AndresGuido9820/sistema-transporte-inteligente
- Notebook 01: https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/01_prediccion_demanda.ipynb
- Notebook 02: https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/02_clasificacion_conduccion.ipynb
- Notebook 03: https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/03_recomendacion_destinos.ipynb
- Capturas: `outputs/screenshots/`
- Videos de demostración: pendiente para el cierre final de entrega.

---

## 9. Bibliografía

- Chicago Data Portal. (s. f.). *CTA - Ridership - Bus Routes - Daily Totals by Route*. https://data.cityofchicago.org/Transportation/CTA-Ridership-Bus-Routes-Daily-Totals-by-Route/jyb9-n7fm
- Kaggle. (s. f.). *Multi-Class Driver Behavior Image Dataset*. https://www.kaggle.com/datasets/arafatsahinafridi/multi-class-driver-behavior-image-dataset/data
- Kaggle. (s. f.). *Travel Recommendation Dataset*. https://www.kaggle.com/datasets/amanmehra23/travel-recommendation-dataset
- Ricci, F., Rokach, L., & Shapira, B. (2015). *Recommender Systems Handbook*. Springer.
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.

# Discusión, Limitaciones y Trabajo Futuro

## 1. Calidad y disponibilidad de datos

El desempeño del sistema depende directamente de la calidad de los datos. En demanda, faltantes o cambios operativos no registrados pueden afectar la predicción. En imágenes, clases desbalanceadas pueden sesgar el clasificador. En recomendación, usuarios nuevos generan el problema de arranque en frío.

## 2. Interpretabilidad

Los modelos de aprendizaje profundo pueden tener buen desempeño, pero suelen ser menos interpretables. Por eso se mantendrán modelos base y análisis de variables para justificar resultados.

## 3. Riesgos en clasificación de conductores

Una predicción incorrecta puede tener consecuencias laborales o reputacionales. El sistema debe usarse como apoyo a revisión humana, no como mecanismo automático de sanción.

## 4. Sesgos en recomendación

El recomendador puede reforzar destinos populares y ocultar rutas menos frecuentes. Para mitigarlo, se recomienda incluir diversidad y exploración controlada en las recomendaciones.

## 5. Trabajo futuro

- Incorporar clima real y eventos urbanos.
- Entrenar con datos reales anonimizados de la empresa.
- Usar modelos secuenciales más robustos para demanda.
- Agregar explicabilidad visual con Grad-CAM en clasificación.
- Evaluar satisfacción de usuarios con pruebas A/B.


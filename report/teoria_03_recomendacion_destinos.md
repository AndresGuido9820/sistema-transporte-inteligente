# Teoría — Sistema de Recomendación de Destinos

## 1. Problema

El objetivo es recomendar destinos personalizados a usuarios de la empresa de transporte con base en su historial de viajes, preferencias y comportamiento de reserva.

El problema puede representarse como una matriz usuario-destino, donde cada celda contiene una interacción: viaje realizado, rating, clic, búsqueda o reserva.

## 2. Filtrado Colaborativo

El filtrado colaborativo recomienda destinos a partir de usuarios con comportamientos similares. Si dos usuarios han viajado a destinos parecidos, es probable que compartan preferencias.

La similitud entre usuarios puede calcularse con coseno:

$$sim(u, v) = \frac{r_u \cdot r_v}{||r_u|| ||r_v||}$$

donde `r_u` y `r_v` son vectores de interacción.

## 3. Recomendación Basada en Contenido

La recomendación basada en contenido usa atributos del destino:

- Ciudad.
- Categoría.
- Clima.
- Tipo de viaje.
- Distancia.
- Precio promedio.

Este enfoque ayuda cuando un usuario tiene pocas interacciones, porque se puede recomendar por preferencias explícitas.

## 4. Enfoque Híbrido

El sistema final combinará filtrado colaborativo y contenido. La puntuación final puede definirse como:

$$score = \alpha \cdot score_{colaborativo} + (1 - \alpha) \cdot score_{contenido}$$

Esto permite equilibrar patrones grupales y preferencias individuales.

## 5. Métricas

Las métricas principales serán:

- Precision@K.
- Recall@K.
- MAP@K opcional.

Estas métricas evalúan si los destinos relevantes aparecen dentro de las primeras recomendaciones.

## 6. Entregables

- Código del recomendador.
- Métricas de evaluación.
- Ejemplos de recomendaciones por usuario.
- Análisis de efectividad.


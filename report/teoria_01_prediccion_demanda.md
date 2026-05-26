# Teoría — Predicción de Demanda de Transporte

## 1. Problema

La predicción de demanda busca estimar cuántos pasajeros o viajes tendrá una ruta en un horizonte futuro. En este proyecto el horizonte será de 30 días por ruta, lo que permite planificar vehículos, conductores, turnos y frecuencia del servicio.

Formalmente, para una ruta `r` y una fecha `t`, se busca aprender una función:

$$\hat{y}_{r,t+h} = f(y_{r,t}, y_{r,t-1}, ..., x_{r,t})$$

donde `h` representa el horizonte de predicción y `x` contiene variables externas como día de la semana, mes, festivos o eventos.

## 2. Variables Temporales

Las variables temporales más importantes serán:

- Día de la semana.
- Mes.
- Indicador de fin de semana.
- Indicador de festivo.
- Rezagos de demanda: `lag_1`, `lag_7`, `lag_14`.
- Medias móviles: `rolling_7`, `rolling_14`.

Estas variables capturan tendencia, estacionalidad semanal y comportamiento reciente.

## 3. Modelos

### 3.1 Modelo base

Se usará una regresión supervisada o Random Forest Regressor como punto de comparación. Este modelo sirve para verificar si las variables construidas explican la demanda sin requerir una arquitectura profunda.

### 3.2 Modelo principal

El modelo principal será una red neuronal MLP o LSTM simple. La MLP trabaja bien cuando se usan rezagos como variables tabulares; la LSTM es adecuada cuando se modela explícitamente una secuencia temporal.

## 4. Métricas

Las métricas principales serán:

- MAE: error absoluto medio.
- RMSE: penaliza errores grandes.
- MAPE: error porcentual medio, útil para comparar rutas con escalas distintas.

## 5. Entregables

- Código de preprocesamiento.
- Modelo entrenado.
- Métricas por ruta.
- Gráficas de demanda real vs. predicción.
- Análisis de tendencia y estacionalidad.


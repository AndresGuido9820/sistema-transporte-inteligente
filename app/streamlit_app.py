from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
import streamlit as st

from transport_ai.common import DATA_DIR, OUTPUTS_DIR
from transport_ai.recommendation import explain_recommendations
from transport_ai.sample_data import generate_all
from transport_ai.vision import classify_image


st.set_page_config(page_title="Sistema Inteligente de Transporte", layout="wide")
st.title("Sistema Inteligente de Transporte")

if not (DATA_DIR / "processed" / "cta_bus_ridership_daily_by_route.csv").exists():
    generate_all()

tab_demand, tab_vision, tab_recs = st.tabs(["Demanda", "Conducción", "Recomendación"])

with tab_demand:
    st.subheader("Predicción de demanda")
    predictions_path = OUTPUTS_DIR / "predictions" / "demand_predictions.csv"
    forecast_path = OUTPUTS_DIR / "predictions" / "demand_forecast_30_days.csv"
    if predictions_path.exists():
        predictions = pd.read_csv(predictions_path)
        route = st.selectbox("Ruta", sorted(predictions["route"].unique()))
        route_df = predictions[predictions["route"] == route]
        st.caption("Validación histórica: demanda real contra demanda estimada.")
        st.line_chart(route_df.set_index("date")[["passengers", "prediction"]])
        if forecast_path.exists():
            forecast = pd.read_csv(forecast_path)
            route_forecast = forecast[forecast["route"] == route]
            st.caption("Pronóstico operativo para los próximos 30 días.")
            st.line_chart(route_forecast.set_index("date")[["forecast_passengers"]])
            st.dataframe(route_forecast, use_container_width=True)
    else:
        st.info("Ejecuta `python scripts/run_all.py` para generar predicciones.")

with tab_vision:
    st.subheader("Clasificación de conducción distractiva")
    uploaded = st.file_uploader("Imagen del conductor", type=["png", "jpg", "jpeg"])
    if uploaded:
        tmp_path = OUTPUTS_DIR / "uploaded_driver_image.png"
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path.write_bytes(uploaded.getbuffer())
        result = classify_image(tmp_path)
        st.image(str(tmp_path), width=320)
        st.metric("Clase", result["label"])
        st.metric("Confianza", f"{result['confidence']:.1%}")
        probabilities = {
            key.replace("probability_", ""): value
            for key, value in result.items()
            if key.startswith("probability_")
        }
        if probabilities:
            st.bar_chart(pd.Series(probabilities).sort_values(ascending=False))
    else:
        st.info("Sube una imagen para clasificarla.")

with tab_recs:
    st.subheader("Recomendación de destinos")
    interactions_path = DATA_DIR / "processed" / "travel_interactions.csv"
    if interactions_path.exists():
        interactions = pd.read_csv(interactions_path)
        user = st.selectbox("Usuario", sorted(interactions["user_id"].unique()))
        st.dataframe(interactions[interactions["user_id"] == user].head(10), use_container_width=True)
        st.dataframe(explain_recommendations(user), use_container_width=True)
    else:
        st.info("No hay interacciones disponibles.")

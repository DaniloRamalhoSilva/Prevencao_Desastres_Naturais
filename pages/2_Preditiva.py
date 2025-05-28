import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Preditiva", layout="wide")
st.header("🤖 Análise Preditiva de Risco")

# Carrega modelo
@st.cache_resource
def load_model(path="models/modelo_risco.joblib"):
    return joblib.load(path)

model = load_model()

# Formulário de entrada
with st.form("form_pred"):
    st.subheader("Entradas do Modelo")
    temperatura = st.number_input("Temperatura (°C)", min_value=-20.0, max_value=60.0, value=25.0)
    umidade = st.slider("Umidade (%)", 0, 100, 50)
    vento = st.number_input("Velocidade do Vento (km/h)", 0.0, 200.0, 10.0)
    submitted = st.form_submit_button("Gerar Predição")

if submitted:
    X = pd.DataFrame([[temperatura, umidade, vento]],
                     columns=["temp", "umidade", "vento"])
    prob = model.predict_proba(X)[0,1]  # probabilidade de alto risco
    classe = model.predict(X)[0]
    st.success(f"Probabilidade de Alto Risco: {prob:.2%}")
    st.info(f"Classe Prevista: {classe}")

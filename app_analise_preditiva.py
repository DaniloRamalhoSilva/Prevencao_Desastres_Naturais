# app_analise_preditiva.py

import streamlit as st
import pandas as pd
import calendar
from pycaret.classification import load_model, predict_model

@st.cache_data
def load_data(path_csv: str) -> pd.DataFrame:
    """
    Carrega o CSV, detecta coluna de data/hora (renomeia para 'data'),
    renomeia 'numero_dias_sem_chuva' -> 'dias_sem_chuva' e 'risco_fogo' -> 'risco',
    extrai 'data_somente' (data sem hora).
    """
    df = pd.read_csv(path_csv, encoding="utf-8", sep=";")
    coluna_data = None
    for col in df.columns:
        nome_minus = col.lower()
        if "data" in nome_minus and "hora" in nome_minus:
            coluna_data = col
            break
        if coluna_data is None and "data" in nome_minus:
            coluna_data = col

    if coluna_data is None:
        raise ValueError("Não foi possível detectar a coluna de data.")

    df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True, errors="coerce")
    df = df.rename(columns={
        coluna_data: "data",
        "numero_dias_sem_chuva": "dias_sem_chuva",
        "risco_fogo": "risco",
    })
    df = df.dropna(subset=["data"])
    df["data_somente"] = df["data"].dt.date
    return df


def display_risk_card(risco: str):
    # Estilos visuais por nível de risco
    estilos = {
        "Baixo":   {"border": "#2ecc71", "bg": "#e9f7ef", "text": "#27ae60", "icon": "✅"},
        "Médio":   {"border": "#f1c40f", "bg": "#fef9e7", "text": "#f39c12", "icon": "⚠️"},
        "Alto":    {"border": "#e67e22", "bg": "#fbeee6", "text": "#d35400", "icon": "🔥"},
        "Muito Alto": {"border": "#c0392b", "bg": "#fdecea", "text": "#e74c3c", "icon": "🚨"},
    }
    # Mensagens personalizadas
    descricoes = {
        "Baixo":       "Baixo risco: condições seguras para atividades externas normais.",
        "Médio":       "Risco moderado: fique atento e evite fogueiras ou queimadas.",
        "Alto":        "Risco alto: limite todas as atividades com fogo e siga orientações locais.",
        "Muito Alto":  "Risco crítico: perigo iminente. Procure abrigo e siga instruções de emergência.",
    }
    if risco not in estilos:
        st.error(f"Nível de risco desconhecido: {risco}")
        return
    style = estilos[risco]
    msg = descricoes.get(risco, "")
    st.markdown(
        f"""
        <div style="border:2px solid {style['border']}; border-radius:8px; padding:16px; background-color:{style['bg']}; margin-bottom:16px;">
            <h2 style="color:{style['text']}; margin:0; font-size:1.5em;">{style['icon']} {risco}</h2>
            <p style="margin:8px 0; color:{style['text']}; font-size:1.1em;">{msg}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render(estado_sel: str, municipio_sel: str, bioma_sel: str, periodo):
    """
    Função que desenha todo o conteúdo da Aba "Análise Preditiva".
    Recebe seleção de Estado, Município, Bioma e Período.
    Não filtra o histórico: usa apenas para obter valores de entrada.
    """
    DATA_PATH = "data/Risco_Fogo.csv"
    MODEL_PATH = 'models\pickle_tuned_rf_pycaret3'

    # Carregar dados
    try:
        df = load_data(DATA_PATH)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return


    # Carregar modelo
    try:
        modelo_risco = load_model(MODEL_PATH)
    except Exception:
        st.error(
            f"Modelo preditivo não encontrado em '{MODEL_PATH}'. Coloque o arquivo pickle do modelo nesse caminho."
        )
        return

    # Parâmetros de entrada (baseados em todo o histórico)
    st.markdown("### 🔮 Parâmetros de Entrada para Previsão de Risco")
    dias_min = int(df["dias_sem_chuva"].min())
    dias_max = int(df["dias_sem_chuva"].max())
    dias_input = st.slider(
        "Dias sem chuva",
        min_value=dias_min,
        max_value=dias_max,
        value=int((dias_min + dias_max) / 2)
    )
    hora_input = st.slider(
        "Hora do dia",
        min_value=0,
        max_value=23,
        value=12
    )
    st.markdown("---")

    # Prever Risco
    if st.button("Prever Risco"):
        if estado_sel == "Todos" or municipio_sel == "Todos" or bioma_sel == "Todos":
            st.error("Selecione Estado, Município e Bioma antes de prever.")
            return

        df_input = pd.DataFrame({
            "municipio": [municipio_sel],
            "estado": [estado_sel],
            "numero_dias_sem_chuva": [dias_input],
            "bioma": [bioma_sel],
            "horario": [hora_input]
        })
        df_input["dia_de_semana"] = df_input["horario"].apply(
            lambda h: calendar.day_name[pd.Timestamp(f"2025-06-06 {h}:00").dayofweek]
        )
        df_proba = predict_model(modelo_risco, data=df_input)
        display_risk_card(df_proba["prediction_label"][0])

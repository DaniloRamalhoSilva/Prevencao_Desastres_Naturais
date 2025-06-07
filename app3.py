# app.py
import streamlit as st
import pandas as pd
from datetime import timedelta

# Importa as funções de renderização de cada aba
from app_analise_descritiva import render as render_descritiva
from app_analise_preditiva import render as render_preditiva
from app_assistente_ia import render as render_assistente

# ----------------------------------------
# 1. Configurações iniciais da página (apenas aqui)
# ----------------------------------------
st.set_page_config(
    page_title="Análise de Risco de Incêndios Florestais",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título geral do app
st.title("🔥 Análise de Risco de Incêndios Florestais")

# ----------------------------------------
# 2. Carrega dados e define filtros globais
# ----------------------------------------
@st.cache_data
def load_data(path_csv: str) -> pd.DataFrame:
    df = pd.read_csv(path_csv, encoding="utf-8", sep=";")
    # detecta coluna de data
    coluna_data = None
    for col in df.columns:
        nome_minus = col.lower()
        if "data" in nome_minus and "hora" in nome_minus:
            coluna_data = col
            break
        if coluna_data is None and "data" in nome_minus:
            coluna_data = col
    df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True, errors="coerce")
    df = df.rename(columns={
        coluna_data: "data",
        "numero_dias_sem_chuva": "dias_sem_chuva",
        "risco_fogo": "risco",
    })
    df = df.dropna(subset=["data"])
    df["data_somente"] = df["data"].dt.date
    return df

DATA_PATH = "data/Risco_Fogo.csv"
df = load_data(DATA_PATH)

# popula opções
lista_estados = sorted(df["estado"].dropna().unique())
lista_biomas = sorted(df["bioma"].dropna().unique())

# cria filtros em colunas
col1, col2, col3, col4 = st.columns(4)
with col1:
    estado_sel = st.selectbox("Estado", options=["Todos"] + lista_estados)
with col2:
    # atualiza municípios conforme estado
    if estado_sel != "Todos":
        lista_municipios = sorted(df[df["estado"] == estado_sel]["municipio"].dropna().unique())
    else:
        lista_municipios = sorted(df["municipio"].dropna().unique())
    municipio_sel = st.selectbox("Município", options=["Todos"] + lista_municipios)
with col3:
    bioma_sel = st.selectbox("Bioma", options=["Todos"] + lista_biomas)
with col4:
    data_min, data_max = df["data_somente"].min(), df["data_somente"].max()
    periodo = st.date_input(
        "Período",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max,
    )

# ----------------------------------------
# 3. Abas do aplicativo
# ----------------------------------------
tab1, tab2, tab3 = st.tabs(["Análise Descritiva", "Análise Preditiva", "Assistente IA"])

with tab1:
    render_descritiva(estado_sel, municipio_sel, bioma_sel, periodo)

with tab2:
    render_preditiva(estado_sel, municipio_sel, bioma_sel, periodo)

with tab3:
    render_assistente()
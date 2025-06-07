# app.py
import streamlit as st
from datetime import timedelta
from app_analise_descritiva import render as render_descritiva, load_data as load_descritiva_data
from app_analise_preditiva import render as render_preditiva
from app_assistente_ia import render as render_assistente
from app_consideracoes import render as render_consideracoes

# ----------------------------------------
# 1. Configurações iniciais da página
# ----------------------------------------
st.set_page_config(
    page_title="Análise de Risco de Incêndios Florestais",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("🔥 Análise de Risco de Incêndios Florestais")

DATA_PATH = "data/Risco_Fogo.csv"

# Função para desenhar filtros comuns
@st.cache_data
def render_filtros():
    df = load_descritiva_data(DATA_PATH)
    lista_estados = sorted(df["estado"].dropna().unique())
    lista_biomas = sorted(df["bioma"].dropna().unique())
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        estado_sel = st.selectbox("Estado", options=["Todos"] + lista_estados)
    with col2:
        if estado_sel != "Todos":
            mun_list = sorted(df[df["estado"] == estado_sel]["municipio"].dropna().unique())
        else:
            mun_list = sorted(df["municipio"].dropna().unique())
        municipio_sel = st.selectbox("Município", options=["Todos"] + mun_list)
    with col3:
        bioma_sel = st.selectbox("Bioma", options=["Todos"] + lista_biomas)
    with col4:
        min_d, max_d = df["data_somente"].min(), df["data_somente"].max()
        periodo = st.date_input(
            "Período",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
        )
    return estado_sel, municipio_sel, bioma_sel, periodo

# ----------------------------------------
# 2. Cria abas do aplicativo
# ----------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Análise Descritiva", "Análise Preditiva", "Assistente IA", "Considerações"
])

with tab1:
    estado_sel, municipio_sel, bioma_sel, periodo = render_filtros()
    render_descritiva(estado_sel, municipio_sel, bioma_sel, periodo)

with tab2:
    estado_sel, municipio_sel, bioma_sel, periodo = render_filtros()
    render_preditiva(estado_sel, municipio_sel, bioma_sel, periodo)

with tab3:
    estado_sel, municipio_sel, bioma_sel, periodo = render_filtros()
    render_assistente(estado_sel, municipio_sel, bioma_sel, periodo)

with tab4:
    # Em Considerações não exibimos filtros
    render_consideracoes()

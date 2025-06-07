# app.py

import streamlit as st

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
# 2. Cria as abas e chama cada render()
# ----------------------------------------
tab1, tab2, tab3 = st.tabs(["Análise Descritiva", "Análise Preditiva", "Assistente IA"])

with tab1:
    render_descritiva()

with tab2:
    render_preditiva()

with tab3:
    render_assistente()

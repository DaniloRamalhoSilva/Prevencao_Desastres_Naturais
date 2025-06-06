import streamlit as st
from menu_lateral import configura_sidebar
from simulador_csv import roda_csv
from perguntas_llm import show_llm_qa     # Se for implementar LLM como terceira aba

st.set_page_config(
    page_title='Análise de Risco de Incêndios',
    page_icon='🔥',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Título principal
st.title("🔥 Análise de Risco de Incêndios Florestais")

# Explicação opcional do sistema
with st.expander("ℹ️ Sobre o sistema"):
    st.markdown("""
    Este sistema permite:
    - 📈 Fazer análises preditivas de risco de incêndio com base em dados históricos;
    - 📂 Trabalhar com arquivos CSV de entrada ou preenchimento online;
    - 💬 Em breve: Perguntas em linguagem natural com ajuda de um modelo de linguagem.

    Desenvolvido com Streamlit e PyCaret.
    """)

# Lê seleção da sidebar
database, file = configura_sidebar()

# Layout com abas
abas = st.tabs(["🧠 Análise Preditiva", "💬 Perguntas com IA (LLM)"])

with abas[0]:
    if database == 'CSV':
        if file:
            roda_csv(file)
        else:
            st.warning("⚠️ Nenhum arquivo CSV foi carregado.")

with abas[1]:
    show_llm_qa()  # Em breve: perguntas com LLM

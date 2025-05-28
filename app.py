import streamlit as st

st.set_page_config(
    page_title="Risco de Desastres",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌎 Bem-vindo ao Terra Segura")
st.markdown("""
Este web-app auxilia na **análise descritiva** e **preditiva** de riscos de desastres naturais.
Use o menu lateral (ou o seletor de páginas) para navegar entre as funcionalidades.
""")
st.image("https://path/to/logo.png", width=200)  # opcional

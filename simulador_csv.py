import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pycaret.classification import load_model, predict_model

def roda_csv(file):
    st.markdown("## 📂 Dados Carregados")

    # Lê CSV já tratado (com 'horario', 'dia_de_semana', etc.)
    df = pd.read_csv(file, sep=';', encoding='utf-8')

    st.dataframe(df.head())

    # Converte data/hora e extrai data e hora separadamente
    df['data_hora_gmt'] = pd.to_datetime(df['data_hora_gmt'], format='%d/%m/%Y %H:%M')
    df['data'] = df['data_hora_gmt'].dt.date
    df['horario'] = df['data_hora_gmt'].dt.strftime('%H:%M')
    df['horario'] = pd.to_datetime(df['horario'], format='%H:%M').dt.hour
    df = df.drop('data_hora_gmt', axis=1)

    # Adiciona o dia da semana
    df['dia_de_semana'] = pd.to_datetime(df['data']).dt.day_name()
    dia_semana_portugues = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    df['dia_de_semana'] = df['dia_de_semana'].map(dia_semana_portugues)
    df = df.drop('data', axis=1)

    # Carrega o modelo treinado
    modelo = load_model('models\pickle_tuned_rf_pycaret3')

    # Aplica a predição
    ypred = predict_model(modelo, data=df)

    st.markdown("## 🔥 Predição de Risco de Incêndio")
    st.dataframe(ypred)

    # Exibe distribuição predita
    st.markdown("### Distribuição de Risco Previsto")
    contagem = ypred['prediction_label'].value_counts().sort_index()
    st.bar_chart(contagem)

    # Permite download
    csv = ypred.to_csv(index=False, sep=';', decimal=',')
    st.download_button("📥 Baixar predições", data=csv, file_name="predicoes_risco.csv", mime="text/csv")

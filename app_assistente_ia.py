# app_assistente_ia.py

import streamlit as st
import os
# from openai import OpenAI   

def render():
    """
    Função que desenha todo o conteúdo da Aba "Assistente IA".
    """
    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown("### 💬 Assistente IA para Incêndios Florestais")

    # Caixa de texto para perguntar
    pergunta = st.text_input("Faça uma pergunta sobre os dados ou predições")
    if st.button("Enviar") and pergunta:
        st.session_state.history.append({"role": "user", "content": pergunta})
        with st.spinner("Pensando…"):
            # Exemplo de integração com OpenAI (descomente e ajuste conforme sua API Key):
            # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            # resposta = client.responses.create(
            #     model="gpt-4o-mini",
            #     instructions="Você é um assistente especializado em risco de incêndios florestais.",
            #     input=st.session_state.history
            # )
            # content = resposta.choices[0].message.content

            # Por enquanto, placeholder:
            content = "Estamos em manutenção"

        st.session_state.history.append({"role": "assistant", "content": content})

    # Exibe histórico de chat
    for chat in st.session_state.history:
        if chat["role"] == "user":
            st.markdown(f"**Você:** {chat['content']}")
        else:
            st.markdown(f"**Assistente:** {chat['content']}")

    st.markdown("---")
    st.markdown(
        """
        **Como usar:**  
        - Pergunte algo como: “Qual o risco previsto para MT hoje?”  
        - Pergunte dados descritivos: “Quantos focos teve Cáceres no último mês?”  
        - Pergunte sobre o modelo preditivo: “Como a umidade afeta o risco?”  

        """
    )

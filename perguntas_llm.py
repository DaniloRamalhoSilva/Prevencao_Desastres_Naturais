import streamlit as st
import os
from openai import OpenAI
from streamlit_chat import message

def show_llm_qa():
    st.markdown("## 💬 Perguntas com IA")
    st.markdown("Faça perguntas sobre os dados ou os riscos de incêndio preditos.")

    # Inicializa cliente da OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ Chave da API OpenAI não encontrada. Defina OPENAI_API_KEY no ambiente.")
        return

    client = OpenAI(api_key=api_key)

    # Inicializa histórico
    if "history" not in st.session_state:
        st.session_state.history = [
            {"role": "system", "content": (
                "Você é um assistente especializado em analisar dados e predições "
                "relacionadas a risco de incêndios florestais. Responda com clareza, "
                "e cite variáveis como bioma, número de dias sem chuva, horário e estado "
                "quando relevante."
            )}
        ]

    # Entrada do usuário
    with st.form("chat_form", clear_on_submit=True):
        query = st.text_input("Digite sua pergunta:")
        submitted = st.form_submit_button("Enviar")

        if submitted and query:
            st.session_state.history.append({"role": "user", "content": query})

            with st.spinner("Pensando..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.history
                )
            content = response.choices[0].message.content
            st.session_state.history.append({"role": "assistant", "content": content})

    # Exibe histórico
    for msg in st.session_state.history[1:]:
        message(msg["content"], is_user=(msg["role"] == "user"))

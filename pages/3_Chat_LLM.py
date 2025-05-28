import streamlit as st
import os
from openai import OpenAI

# carrega chave
api_key = os.getenv("OPENAI_API_KEY")
client  = OpenAI(api_key=api_key)

st.set_page_config(page_title="Chat LLM", layout="wide")
st.header("💬 Perguntas e Respostas com LLM")

if "history" not in st.session_state:
    # você pode inserir aqui uma mensagem de sistema:
    st.session_state.history = [
        {"role": "system", "content": "Por enquanto você é livre para responder."}
    ]

# entrada do usuário
query = st.text_input("Digite sua pergunta sobre os dados ou predições")
if st.button("Enviar") and query:
    st.session_state.history.append({"role": "user", "content": query})

    with st.spinner("Pensando…"):
        # use o namespace chat.completions.create
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.history
        )

    # agora você tem .choices
    content = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": content})

# exibição do histórico
from streamlit_chat import message
for msg in st.session_state.history:
    is_user = msg["role"] == "user"
    message(msg["content"], is_user=is_user)

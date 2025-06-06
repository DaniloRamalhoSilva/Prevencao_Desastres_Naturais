import streamlit as st

def configura_sidebar():
    with st.sidebar:
        c1, c2 = st.columns([0.25, 0.75])
        #c1.image('./images/logo_fiap.png', width=80)
        c2.markdown("### Incêndios Florestais\n#### 🔥 Prevenção e Análise")

        st.markdown("---")
        st.markdown("#### Fonte dos Dados")
        db = st.radio(
            'Escolha como os dados serão carregados:',
            ('CSV', 'Online'),
            horizontal=True
        )

        file = None
        if db == 'CSV':
            st.info('Faça upload de um arquivo CSV com os dados de entrada.')
            file = st.file_uploader('Selecione o arquivo CSV', type='csv')

        st.markdown("---")
        st.caption("Desenvolvido por Fiap | v1.0")

    return db, file

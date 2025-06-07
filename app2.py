# app_descritiva_e_preditiva.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pickle
from datetime import timedelta

# ----------------------------------------
# 1. Configurações iniciais da página
# ----------------------------------------
st.set_page_config(
    page_title="Análise de Risco de Incêndios Florestais",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔥 Análise de Risco de Incêndios Florestais")

# ----------------------------------------
# 2. Carregar dados (detectando coluna de data)
# ----------------------------------------
@st.cache_data
def load_data(path_csv: str) -> pd.DataFrame:
    """
    Carrega o CSV e tenta detectar automaticamente a coluna de data.
    Suporta campos como 'data_hora_gmt' ou simplesmente 'data_hora'.
    Renomeia-a para 'data' internamente.
    Também renomeia:
      - numero_dias_sem_chuva  ➞ dias_sem_chuva
      - risco_fogo             ➞ risco
    """
    # 1) Lê tudo primeiro (sem parse_dates), só para obter colunas
    df = pd.read_csv(path_csv, encoding="utf-8", sep=";")
    
    # 2) Detecta qual coluna contém a data/hora (procura "data" no nome)
    coluna_data = None
    for col in df.columns:
        nome_minusculo = col.lower()
        # Se contiver "data" e "hora" (ou apenas "data"), considera como coluna de data
        if "data" in nome_minusculo and "hora" in nome_minusculo:
            coluna_data = col
            break
        if coluna_data is None and "data" in nome_minusculo:
            # caso não encontre "data"+"hora", tenta só "data"
            coluna_data = col
    
    if coluna_data is None:
        raise ValueError(
            "Não foi possível detectar automaticamente qual coluna é a de data. "
            "Verifique o cabeçalho do CSV."
        )
    
    # 3) Converte a coluna de data para datetime (dayfirst=True para dd/mm/aaaa)
    df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True, errors="coerce")
    
    # 4) Renomeia as colunas para nomes que usaremos internamente
    df = df.rename(columns={
        coluna_data: "data",
        "numero_dias_sem_chuva": "dias_sem_chuva",
        "risco_fogo": "risco",
    })
    
    # 5) Verifica se houve linhas sem data válida e remove
    df = df.dropna(subset=["data"])
    
    # 6) Extrai só a data (sem hora) para agrupar facilmente
    df["data_somente"] = df["data"].dt.date
    
    return df

# 2.1. Ajuste o nome do arquivo CSV conforme sua realidade
DATA_PATH = "data/Risco_Fogo.csv"
df = load_data(DATA_PATH)

# ----------------------------------------
# 3. Carregar modelo preditivo (arquivo .pkl)
# ----------------------------------------
@st.cache_data
def load_model(path_modelo: str):
    """
    Carrega o modelo de classificação/regressão treinado
    (arquivo pickle). Retorna o objeto do modelo.
    """
    with open(path_modelo, "rb") as f:
        modelo = pickle.load(f)
    return modelo

# Ajuste o caminho conforme a localização do seu .pkl
MODEL_PATH = "models/modelo_risco.pkl"
try:
    modelo_risco = load_model(MODEL_PATH)
except FileNotFoundError:
    modelo_risco = None

# ----------------------------------------
# 4. Componentes principais via abas (tabs)
# ----------------------------------------
tab1, tab2, tab3 = st.tabs(["Análise Descritiva", "Análise Preditiva", "Assistente IA"])

# ==============================
# Aba 1: Análise Descritiva
# ==============================
with tab1:
    # ----------------------------------------
    # 3. Sidebar / Filtros (para Análise Descritiva)
    # ----------------------------------------
    with st.sidebar:
        st.header("Filtros - Análise Descritiva")

        # 3.1. Filtro por Estado
        lista_estados = sorted(df["estado"].dropna().unique())
        estado_selecionado = st.selectbox("Estado", options=["Todos"] + lista_estados)

        # 3.2. Filtro por Município (depende do estado)
        if estado_selecionado != "Todos":
            df_estado = df[df["estado"] == estado_selecionado]
            lista_municipios = sorted(df_estado["municipio"].dropna().unique())
        else:
            lista_municipios = sorted(df["municipio"].dropna().unique())
        municipio_selecionado = st.selectbox("Município", options=["Todos"] + lista_municipios)

        # 3.3. Filtro por Bioma
        lista_biomas = sorted(df["bioma"].dropna().unique())
        bioma_selecionado = st.selectbox("Bioma", options=["Todos"] + lista_biomas)

        # 3.4. Filtro por Data (período)
        data_min = df["data_somente"].min()
        data_max = df["data_somente"].max()
        periodo = st.date_input(
            "Período",
            value=(data_min, data_max),
            min_value=data_min,
            max_value=data_max,
        )

    # ----------------------------------------
    # 4. Aplicar filtros ao DataFrame
    # ----------------------------------------
    mask = pd.Series(True, index=df.index)

    if estado_selecionado != "Todos":
        mask &= df["estado"] == estado_selecionado

    if municipio_selecionado != "Todos":
        mask &= df["municipio"] == municipio_selecionado

    if bioma_selecionado != "Todos":
        mask &= df["bioma"] == bioma_selecionado

    data_inicio, data_fim = periodo
    mask &= (df["data_somente"] >= data_inicio) & (df["data_somente"] <= data_fim)

    df_filtrado = df[mask].copy()

    # ----------------------------------------
    # 5. Métricas Principais (KPIs)
    # ----------------------------------------
    st.markdown("## 📊 KPIs Descritivos")
    col1, col2, col3, col4 = st.columns(4)

    # 5.1. Média de dias sem chuva
    if not df_filtrado.empty:
        media_dias = df_filtrado["dias_sem_chuva"].mean()
        col1.metric("Média dias sem chuva", f"{media_dias:.1f}")
    else:
        col1.metric("Média dias sem chuva", "—")

    # 5.2. Total de registros (ex: total de pontos no período)
    total_registros = len(df_filtrado)
    col2.metric("Total de Registros", f"{total_registros:,}")

    # 5.3. Última data registrada (dentro do filtro)
    if not df_filtrado.empty:
        ultima_data = df_filtrado["data_somente"].max()
        col3.metric("Última Data Registrada", ultima_data.strftime("%d/%m/%Y"))
    else:
        col3.metric("Última Data Registrada", "—")

    # 5.4. Risco médio (nos dados filtrados)
    if not df_filtrado.empty:
        media_risco = df_filtrado["risco"].mean()
        col4.metric("Risco Médio", f"{media_risco:.2f}")
    else:
        col4.metric("Risco Médio", "—")

    st.markdown("---")

    # ----------------------------------------
    # 6. Gráficos Descritivos
    # ----------------------------------------
    st.markdown("### 📈 Evolução Temporal do Nº de Registros (Últimos 30 dias)")

    if not df_filtrado.empty:
        # Para a lógica de “últimos 30 dias”, definimos o intervalo
        data_fim_periodo = data_fim
        data_inicio_30 = data_fim_periodo - timedelta(days=29)

        df_30dias = df_filtrado[df_filtrado["data_somente"] >= data_inicio_30]
        # Agrupar por dia
        serie_agregada = (
            df_30dias.groupby("data_somente")
            .agg(contagem=("risco", "count"))
            .reset_index()
        )

        # Se houver dias faltantes, preenchemos com zero
        idx = pd.date_range(start=data_inicio_30, end=data_fim_periodo)
        serie_agregada = (
            serie_agregada
            .set_index("data_somente")
            .reindex(idx, fill_value=0)
            .rename_axis("data_somente")
            .reset_index()
        )

        fig1 = px.line(
            serie_agregada,
            x="data_somente",
            y="contagem",
            labels={"data_somente": "Data", "contagem": "Nº de Registros"},
            title="Focos de Incêndio (nº de registros) - Últimos 30 dias"
        )
        fig1.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.write("Nenhum dado para mostrar no período selecionado.")

    st.markdown("### 📊 Top 5 Municípios com Mais Registros no Período")

    if not df_filtrado.empty:
        top_municipios = (
            df_filtrado["municipio"]
            .value_counts()
            .reset_index()
            .rename(columns={"index": "municipio", "municipio": "contagem"})
            .head(5)
        )
        fig2 = px.bar(
            top_municipios,
            x="contagem",
            y="municipio",
            orientation="h",
            labels={"contagem": "Nº de Registros", "municipio": "Município"},
            title="Top 5 Municípios com Mais Registros"
        )
        fig2.update_layout(
            margin=dict(t=40, b=20, l=20, r=20),
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.write("Nenhum registro encontrado para os filtros selecionados.")

    # ----------------------------------------
    # 7. Mapa de Risco por Região (Placeholder)
    # ----------------------------------------
    st.markdown("### 🗺️ Mapa de Risco por Região (placeholder)")

    st.info(
        """
        Para exibir um mapa de calor/choropleth por município ou estado, você precisará de:
        1) GeoJSON ou shapefile de limites municipais/estaduais do Brasil (ex.: IBGE).  
        2) Fazer merge entre seu DataFrame filtrado e o GeoDataFrame (p. ex., usando nome de município).  
        3) Plotar com `plotly.express.choropleth`, `folium` ou `geopandas`.  
        Veja exemplo (com Plotly):
        ```python
        import geopandas as gpd
        # geo = gpd.read_file("municipios.geojson")
        # df_agregado = df_filtrado.groupby("municipio")["risco"].mean().reset_index()
        # merged = geo.merge(df_agregado, left_on="NM_MUN", right_on="municipio", how="left")
        # fig_map = px.choropleth(
        #     merged, 
        #     geojson=merged.geometry, 
        #     locations=merged.index, 
        #     color="risco", 
        #     hover_name="municipio",
        #     projection="mercator",
        # )
        # fig_map.update_geos(fitbounds="locations", visible=False)
        # st.plotly_chart(fig_map, use_container_width=True)
        ```
        """
    )

    # ----------------------------------------
    # 8. Observações Finais
    # ----------------------------------------
    st.markdown("---")
    st.markdown(
        """
        **Observações Importantes (Análise Descritiva):**
        - Confirme o nome exato do seu CSV (no código usamos `DATA_PATH = "data/Risco_Fogo.csv"`).  
        - A função `load_data` tenta achar automaticamente qual coluna contém a data (procura “data” + “hora”).  
          - Se o seu arquivo tiver outro nome de coluna (por exemplo, apenas “data”), ela também captura.  
          - Caso não encontre nada parecido com “data” no cabeçalho, vai disparar um `ValueError`.  
        - Se você tiver outras colunas com nomes diferentes, basta ajustar o mapeamento em `df.rename(...)`.  
        - Para melhorar performance em bases grandes, mantenha o decorator `@st.cache_data` na função de carregamento.  
        - Use `pip install streamlit pandas numpy plotly` antes de rodar.  
        - Para executar:  
          ```bash
          streamlit run app_descritiva_e_preditiva.py
          ```
        """
    )

# ==============================
# Aba 2: Análise Preditiva
# ==============================
with tab2:
    st.header("🔮 Análise Preditiva de Risco de Incêndios")

    if modelo_risco is None:
        st.error(
            "Modelo preditivo não encontrado em '{}'.\n"
            "Por favor coloque o arquivo pickle do modelo nesse caminho.".format(MODEL_PATH)
        )
    else:
        # 2.1. Slider para 'Dias sem chuva' (baseado no dataset)
        dias_min = int(df["dias_sem_chuva"].min())
        dias_max = int(df["dias_sem_chuva"].max())
        dias_input = st.slider(
            "Dias sem chuva", 
            min_value=dias_min, 
            max_value=dias_max, 
            value=int(df["dias_sem_chuva"].median())
        )

        # 2.2. Slider para 'Hora do dia' (0 a 23)
        hora_input = st.slider(
            "Hora do dia", 
            min_value=0, 
            max_value=23, 
            value=12
        )

        # 2.3. Slider para 'Umidade relativa (%)'
        umidade_input = st.slider(
            "Umidade relativa (%)", 
            min_value=0, 
            max_value=100, 
            value=50
        )

        st.markdown("---")

        # 2.4. Botão para disparar a predição
        if st.button("Prever Risco"):
            # 2.5. Montar DataFrame de entrada para o modelo
            # Ajuste os nomes das colunas conforme o que seu modelo espera
            X_novo = pd.DataFrame({
                "dias_sem_chuva": [dias_input],
                "hora": [hora_input],
                "umidade_relativa": [umidade_input]
            })

            # 2.6. Prever classe e probabilidades
            try:
                probas = modelo_risco.predict_proba(X_novo)[0]
                classes = modelo_risco.classes_
            except Exception as e:
                st.error("Erro ao executar predição: {}".format(e))
                probas = None
                classes = None

            if probas is not None:
                # 2.7. Montar resultado em DataFrame para exibir gráfico
                df_proba = pd.DataFrame({
                    "classe": classes,
                    "probabilidade": probas
                }).sort_values(by="probabilidade", ascending=False)

                # 2.8. Encontrar a classe de maior probabilidade
                classe_predita = df_proba.iloc[0]["classe"]
                proba_predita = df_proba.iloc[0]["probabilidade"]

                # Exibir cartão de resultado
                st.markdown(
                    f"""
                    <div style="border: 2px solid #FF4500; border-radius: 8px; padding: 16px; background-color:#FFF5F0;">
                        <h2 style="color:#FF4500; margin:0;">
                            🔥 {classe_predita.upper()}
                        </h2>
                        <p style="margin:4px 0;">
                            Risco de incêndio – atenção redobrada na região!
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # 2.9. Mostrar gráfico de barras horizontal com probabilidades
                fig_proba = px.bar(
                    df_proba,
                    x="probabilidade",
                    y="classe",
                    orientation="h",
                    labels={"probabilidade": "Probabilidade", "classe": "Classe"},
                    title="Probabilidades por Classe de Risco"
                )
                fig_proba.update_layout(margin=dict(t=40, b=20, l=40, r=20))
                st.plotly_chart(fig_proba, use_container_width=True)

# ==============================
# Aba 3: Assistente IA
# ==============================
with tab3:
    st.header("💬 Assistente IA")

    # Placeholder para integração com modelo LLM
    # Você pode usar `st.text_input` junto com `openai.ChatCompletion.create(...)`, ou
    # integrar qualquer outra API de LLM que preferir.

    if "history" not in st.session_state:
        st.session_state.history = []

    pergunta = st.text_input("Faça uma pergunta sobre os dados ou predições")
    if st.button("Enviar") and pergunta:
        st.session_state.history.append({"role": "user", "content": pergunta})
        with st.spinner("Pensando…"):
            # Exemplo de integração com OpenAI (ajuste seu código conforme necessário):
            # resposta = openai.ChatCompletion.create(
            #     model="gpt-4o-mini",
            #     messages=st.session_state.history
            # )
            # content = resposta.choices[0].message.content

            # Placeholder: resposta fixa
            content = "Aqui vai a resposta da LLM (integre sua API de preferência)."
            
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
        
        _Obs.: ajuste esta aba para chamar de fato sua API de LLM (OpenAI, Hugging Face, etc.)_
        """
    )


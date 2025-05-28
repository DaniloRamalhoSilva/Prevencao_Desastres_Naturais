import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Descritiva", layout="wide")

st.header("📊 Análise Descritiva")

# 1. Carregamento de dados
@st.cache_data
def load_data():
    return pd.read_csv("data/eventos.csv", parse_dates=["data"])

df = load_data()

# 2. Filtros
with st.sidebar.expander("Filtros Descritiva", expanded=True):
    tipos = st.multiselect("Tipos de Desastre", df.tipo.unique(), default=df.tipo.unique())
    periodo = st.date_input("Período", [df.data.min(), df.data.max()])

df_filtro = df.query(
    "tipo in @tipos and @periodo[0] <= data <= @periodo[1]"
)

# 3. Métricas rápidas
col1, col2, col3 = st.columns(3)
col1.metric("Eventos", len(df_filtro))
col2.metric("Área Total (ha)", int(df_filtro.area.sum()))
col3.metric("Vítimas", int(df_filtro.vitimas.sum()))

# 4. Série temporal
st.subheader("Eventos por Dia")
serie = df_filtro.groupby("data").size().rename("contagem")
st.line_chart(serie)

# 5. Mapa interativo
st.subheader("Mapa de Ocorrências")
mapa = pdk.Deck(
    map_style="MAPBOX://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=df_filtro.lat.mean(),
        longitude=df_filtro.lon.mean(),
        zoom=5
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=df_filtro,
            get_position=["lon", "lat"],
            get_radius="area * 10",
            pickable=True,
            tooltip=True
        )
    ]
)
st.pydeck_chart(mapa)

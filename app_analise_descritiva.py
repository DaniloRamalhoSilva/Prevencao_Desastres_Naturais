# app_analise_descritiva.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

@st.cache_data
def load_data(path_csv: str) -> pd.DataFrame:
    # mesma função de carregamento utilizada em app.py
    df = pd.read_csv(path_csv, encoding="utf-8", sep=";")
    coluna_data = None
    for col in df.columns:
        nome_minus = col.lower()
        if "data" in nome_minus and "hora" in nome_minus:
            coluna_data = col
            break
        if coluna_data is None and "data" in nome_minus:
            coluna_data = col
    df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True, errors="coerce")
    df = df.rename(columns={
        coluna_data: "data",
        "numero_dias_sem_chuva": "dias_sem_chuva",
        "risco_fogo": "risco",
    })
    df = df.dropna(subset=["data"])
    df["data_somente"] = df["data"].dt.date
    return df


def render(estado_sel: str, municipio_sel: str, bioma_sel: str, periodo):
    # Carrega dados
    df = load_data("data/Risco_Fogo.csv")

    # Aplica filtros recebidos
    mask = pd.Series(True, index=df.index)
    if estado_sel != "Todos": mask &= df["estado"] == estado_sel
    if municipio_sel != "Todos": mask &= df["municipio"] == municipio_sel
    if bioma_sel != "Todos": mask &= df["bioma"] == bioma_sel
    data_inicio, data_fim = periodo
    mask &= (df["data_somente"] >= data_inicio) & (df["data_somente"] <= data_fim)
    df_filtrado = df[mask].copy()

    # 4) KPIs Descritivos
    st.markdown("## 📊 KPIs Descritivos")
    col1, col2, col3, col4 = st.columns(4)

    # Média dias sem chuva
    if not df_filtrado.empty:
        media_dias = df_filtrado["dias_sem_chuva"].mean()
        col1.metric("Média dias sem chuva", f"{media_dias:.1f}")
    else:
        col1.metric("Média dias sem chuva", "—")

    # Total registros
    total_reg = len(df_filtrado)
    col2.metric("Total de Registros", f"{total_reg:,}")

    # Última data registrada
    if not df_filtrado.empty:
        ultima_data = df_filtrado["data_somente"].max()
        col3.metric("Última Data Registrada", ultima_data.strftime("%d/%m/%Y"))
    else:
        col3.metric("Última Data Registrada", "—")

    # Risco médio
    if not df_filtrado.empty:
        media_risco = df_filtrado["risco"].mean()
        col4.metric("Risco Médio", f"{media_risco:.2f}")
    else:
        col4.metric("Risco Médio", "—")

    st.markdown("---")

    # 5) Gráfico: Evolução Temporal (últimos 30 dias)
    st.markdown("### 📈 Evolução Temporal do Nº de Registros (Últimos 30 dias)")
    if not df_filtrado.empty:
        data_fim_per = data_fim
        data_inicio_30 = data_fim_per - timedelta(days=29)
        df_30dias = df_filtrado[df_filtrado["data_somente"] >= data_inicio_30]
        serie_ag = (
            df_30dias.groupby("data_somente")
            .agg(contagem=("risco", "count"))
            .reset_index()
        )

        idx = pd.date_range(start=data_inicio_30, end=data_fim_per)
        serie_ag = (
            serie_ag
            .set_index("data_somente")
            .reindex(idx, fill_value=0)
            .rename_axis("data_somente")
            .reset_index()
        )

        fig1 = px.line(
            serie_ag,
            x="data_somente",
            y="contagem",
            labels={"data_somente": "Data", "contagem": "Nº de Registros"},
            title="Focos de Incêndio (nº de registros) - Últimos 30 dias"
        )
        fig1.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.write("Nenhum dado para mostrar no período selecionado.")

    # 6) Gráfico: Top 5 Municípios
    st.markdown("### 📊 Top 5 Municípios com Mais Registros no Período")
    if not df_filtrado.empty:
        top_mun = (
            df_filtrado["municipio"]
            .value_counts()
            .reset_index()
            .rename(columns={"index": "municipio", "municipio": "contagem"})
            .head(5)
        )
        fig2 = px.bar(
            top_mun,
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

    # 7) Mapa de Risco (placeholder)
    #st.markdown("### 🗺️ Mapa de Risco por Região (placeholder)")
    #st.info(
    #    """
    #    Para exibir um mapa de calor/choropleth por município ou estado, é preciso:
    #    1) GeoJSON ou shapefile de limites municipais/estaduais do Brasil (ex.: IBGE).  
    #    2) Fazer merge do DataFrame filtrado com o GeoDataFrame (por município).  
    #    3) Plotar com `px.choropleth`, `folium` ou `geopandas`.  
    #    
    #    Exemplo (Plotly):
    #    ```python
    #    import geopandas as gpd
    #    # geo = gpd.read_file("municipios.geojson")
    #    # df_ag = df_filtrado.groupby("municipio")["risco"].mean().reset_index()
    #    # merged = geo.merge(df_ag, left_on="NM_MUN", right_on="municipio", how="left")
    #    # fig_map = px.choropleth(
    #    #     merged, 
    #    #     geojson=merged.geometry, 
    #    #     locations=merged.index, 
    #    #     color="risco", 
    #    #     hover_name="municipio",
    #    #     projection="mercator"
    #    # )
    #    # fig_map.update_geos(fitbounds="locations", visible=False)
    #    # st.plotly_chart(fig_map, use_container_width=True)
    #    ```
    #    """
    #)


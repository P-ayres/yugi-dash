import streamlit as st
import pandas as pd
import plotly.express as px
from yugi_dash.app.utils import dataloader


st.set_page_config(
    page_title="Atributos dos Monstros",
    page_icon="src/yugi_dash/app/data/icon.png",
    layout="wide",
)

df = dataloader.load_data()

st.markdown("## 🀆 Distribuição de Atributos dos Monstros 🀆 ")
st.markdown("```Este gráfico mostra a distribuição de atributos dos cards do tipo Monstro.```")
st.markdown("```Cada fatia do gráfico representa a proporção de cards com um determinado atributo.```")
st.markdown("```Dê 2 cliques em um atributo da legenda para destaca-la, clique uma vez omiti-la/reexibi-la.```")

filtered_df = df[df["type"].str.contains("MONSTER", na=False)].copy()

attribute_df = (
    filtered_df.dropna(subset=["attribute"])
    .groupby("attribute")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

fig = px.pie(
    attribute_df,
    values="count",
    names="attribute",
    title="Distribuição de Atributos dos Monstros",
)

st.plotly_chart(fig, use_container_width=True)
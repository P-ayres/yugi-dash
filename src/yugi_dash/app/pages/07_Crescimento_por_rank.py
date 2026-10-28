import streamlit as st
import pandas as pd
import plotly.express as px
from yugi_dash.app.utils import dataloader

st.set_page_config(
    page_title="Crescimento por Rank",
    page_icon="src/yugi_dash/app/data/icon.png",
    layout="wide",
)

df = dataloader.load_data()

st.markdown("### 🀆 Crescimento de atributos dos monstros por rank 🀆 ")
st.markdown("```Gráfico que evidencia o crescimento médio de ataque e defesa dos monstros por rank.```")
st.markdown("```Clique na legenda para destacar ou omitir uma das linhas do gráfico.```")

monster_df = df[df["type"].str.contains("MONSTER", na=False)].copy()

monster_df["rank"] = (
    monster_df["rank"]
    .astype(str)
    .str.extract(r"(\d+)", expand=False)
    .astype(float)
)

for col in ["attack", "defense"]:
    monster_df[col] = (
        monster_df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.extract(r"(-?\d+)", expand=False)
        .astype(float)
    )

rank_growth = (
    monster_df
    .dropna(subset=["rank", "attack", "defense"])
    .groupby("rank", as_index=False)[["attack", "defense"]]
    .mean().round()
    .sort_values("rank")
)

fig = px.line(
    rank_growth,
    x="rank",
    y=["attack", "defense"],
    markers=True,
    title="Crescimento de ataque e defesa por rank",
    labels={
        "rank": "Rank",
        "value": "Média do atributo",
        "variable": "Status",
    },
)

fig.update_layout(
    xaxis_title="Rank",
    yaxis_title="Valor médio",
    legend_title_text="Estatística",
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)
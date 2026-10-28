import streamlit as st
import pandas as pd
import plotly.express as px
from yugi_dash.app.utils import dataloader

st.set_page_config(
    page_title="Magias e Armadilhas",
    page_icon="src/yugi_dash/app/data/icon.png",
    layout="wide",
)

df = dataloader.load_data()

st.markdown("## 🀆 Magias e Armadilhas 🀆")
st.markdown("Relação de magias e armadilhas com os subtipos das cartas.")
st.badge("```O subtipo define a forma de utilização da carta durante um duelo.```")
st.markdown("```Visualização exploratória de Magias e Armadilhas: clique nos setores para explorar os subtipos, raridades e sets, chegando até os cards.```")

spell_df = df.copy()

spell_df["type"] = spell_df["type"].astype(str).str.upper().str.strip()
spell_df["sub_type"] = (
    spell_df["sub_type"]
    .replace(r"^\s*$", pd.NA, regex=True)
    .fillna("undefined")
)

spell_trap = spell_df[spell_df["type"].isin(["SPELL", "TRAP"])].copy()

rarity_col = "rarity"
set_col = "set_name" if "set_name" in spell_trap.columns else "set"
card_col = "name" if "name" in spell_trap.columns else "card_name"

required = ["type", "sub_type", rarity_col, set_col, card_col]
missing = [c for c in required if c not in spell_trap.columns]
if missing:
    st.error(f"Missing required columns for treemap: {missing}")
    st.stop()

for c in [rarity_col, set_col, card_col]:
    spell_trap[c] = (
        spell_trap[c]
        .replace(r"^\s*$", pd.NA, regex=True)
        .fillna("undefined")
        .astype(str)
    )

plot_df = (
    spell_trap.groupby(
        ["type", "sub_type", rarity_col, set_col, card_col],
        as_index=False,
        dropna=False,
    )
    .size()
    .rename(columns={"size": "count"})
)

for card_type, title in [("SPELL", "SPELL"), ("TRAP", "TRAP")]:
    type_df = plot_df[plot_df["type"] == card_type]

    if type_df.empty:
        st.info(f"No data for {card_type}.")
        continue

    fig = px.treemap(
        type_df,
        path=["type", "sub_type", rarity_col, set_col, card_col],
        values="count",
        color_continuous_scale="type",
        hover_data={"count": True},
    )

    st.plotly_chart(fig, use_container_width=True)
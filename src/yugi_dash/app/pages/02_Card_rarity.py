import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("src/yugi_dash/app/data/yugioh.csv")
rarity_df = df.groupby("rarity").size().reset_index(name="count").sort_values(by="count", ascending=False)

st.set_page_config(
    page_title="🀆 Card Rarity",
    page_icon="🀆",
)

st.markdown("# Card Rarity Analysis")
st.write("This page provides an analysis of card rarity in the Yu-Gi-Oh! dataset.")

fig = px.bar(rarity_df, x="rarity", y="count", title="Card Rarity Distribution", labels={"rarity": "Rarity", "count": "Count"})
st.plotly_chart(fig)
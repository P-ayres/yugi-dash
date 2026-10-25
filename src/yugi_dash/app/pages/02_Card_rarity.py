import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv("src/yugi_dash/app/data/yugioh.csv")
    return df

df = load_data()

st.set_page_config(
    page_title="🀆 Card Rarity",
    page_icon="🀆",
)

st.markdown("# Card Rarity Analysis")
st.write("This page provides an analysis of card rarity in the Yu-Gi-Oh! dataset.")

type_options = sorted(df["type"].dropna().unique().tolist())

selected_type = st.menu_button(
    "Filter by card type",
    options=type_options,
)

filtered_df = df[df["type"] == selected_type]

rarity_df = (
    filtered_df.groupby("rarity")
    .size()
    .reset_index(name="count")
    .sort_values(by="count", ascending=False)
)

chart_title = f"Card Rarity Distribution - {selected_type}"

if selected_type is None:
    st.warning("Please select a card type to view the rarity distribution.")

fig = px.bar(
    rarity_df,
    x="rarity",
    y="count",
    title=chart_title,
    labels={"rarity": "Rarity", "count": "Count"},
)

st.plotly_chart(fig, use_container_width=True)
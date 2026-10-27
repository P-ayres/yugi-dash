import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Volatilidade dos cards",
    page_icon="src/yugi_dash/app/data/icon.png",
    layout="wide",
)

@st.cache_data
def load_data():
    return pd.read_csv("src/yugi_dash/app/data/yugioh.csv")


df = load_data()

st.markdown("## 🀆 Volatilidade dos cards 🀆")
st.markdown("Distribuição dos cards por nível de volatilidade, com filtros por tipo e raridade.")
st.badge("```A volatilidade é uma medida de quanto o preço de um card pode variar ao longo do tempo.```")

required_columns = {"volatility", "type", "rarity", "price"}
missing_columns = required_columns - set(df.columns)
if missing_columns:
    st.error(f"Colunas ausentes no dataset: {', '.join(sorted(missing_columns))}")
    st.stop()

df["volatility"] = (
    df["volatility"]
    .astype(str)
    .str.strip()
    .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
)

df["price"] = (
    df["price"]
    .astype(str)
    .str.replace(r"[^\d,.\-]", "", regex=True)
)

df["price"] = pd.to_numeric(df["price"], errors="coerce")

filtered_df = df.copy()
filtered_df = filtered_df.dropna(subset=["volatility"])

if filtered_df.empty:
    st.warning("Nenhum card encontrado com os filtros selecionados.")
    st.stop()


sunburst_df = filtered_df.dropna(subset=["volatility", "rarity", "price"]).copy()
sunburst_df = sunburst_df[sunburst_df["price"] >= 0]

if sunburst_df.empty:
    st.warning("Sem dados suficientes para o gráfico sunburst.")
else:
    sunburst_agg = (
        sunburst_df.groupby(["volatility", "rarity"], as_index=False)
        .agg(
            total_price=("price", "sum"),
            cards=("price", "size"),
            avg_price=("price", "mean"),
        )
    )

    fig_sunburst = px.sunburst(
        sunburst_agg,
        path=["volatility", "rarity"],
        values="total_price",
        color="volatility",
        color_discrete_sequence=["#7C4DFF", "#5E35B1", "#4527A0", "#B39DDB"],
        title="Sunburst: Volatilidade → Raridade (soma dos preços)",
        hover_data={"cards": True, "avg_price": ":.2f", "total_price": ":.2f"},
    )

    fig_sunburst.update_layout(template="plotly_white")
    st.plotly_chart(fig_sunburst, use_container_width=True)
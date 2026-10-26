
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Preço dos cards",
    layout="wide",
)


@st.cache_data
def load_data():
    return pd.read_csv("src/yugi_dash/app/data/yugioh.csv")


df = load_data()

st.markdown("# Preço médio dos cards por raridade")
st.write(
    "Use o filtro de preço para visualizar a distribuição de preços médios por raridade. "
    "Use o seletor de faixa de preço para filtrar os cards."
)


required_columns = {"rarity", "price"}
missing_columns = required_columns - set(df.columns)

df["price"] = pd.to_numeric(df["price"], errors="coerce")

price_df = df.dropna(subset=["rarity", "price"]).copy()
price_df = price_df[price_df["price"] >= 0]


min_price = float(price_df["price"].min())
max_price = float(price_df["price"].max())

st.subheader("Filtragem por preço")

price_range = st.slider(
    "Selecione a faixa de preço usando o controle deslizante abaixo:",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
    step=max((max_price - min_price) / 100, 0.01),
    format="%.2f",
)

filtered_df = price_df[
    price_df["price"].between(
        price_range[0],
        price_range[1],
    )
]

st.caption(
    f"Price range: {price_range[0]:.2f} – "
    f"{price_range[1]:.2f}"
)

rarity_prices = (
    filtered_df.groupby("rarity")["price"]
    .mean()
    .sort_values(ascending=False)
)

col1, col2 = st.columns(2)

with col1:
    st.metric("Cartas na faixa - ", len(filtered_df))

with col2:
    st.metric(
        "Preço médio",
        f"{filtered_df['price'].mean():.2f}",
    )

fig, ax = plt.subplots(figsize=(12, 6))

rarity_prices.plot(
    kind="bar",
    ax=ax,
    color="#7C4DFF",
)

ax.set_title("Preço médio por raridade")
ax.set_xlabel("Rarity")
ax.set_ylabel("Average Price")
ax.tick_params(axis="x", labelrotation=45)

fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

with st.expander("Ver tabela de preços"):
    st.dataframe(
        filtered_df.sort_values("price", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

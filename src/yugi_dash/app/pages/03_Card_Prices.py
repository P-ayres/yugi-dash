
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
    "O seletor de faixa de preço permite ajustar os limites mínimo e máximo para a análise."
)


required_columns = {"rarity", "price"}
missing_columns = required_columns - set(df.columns)

df["price"] = (
    df["price"]
    .astype(str)
    .str.replace(r"[^\d,.\-]", "", regex=True)        
)

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
    format="%.2f",
)

filtered_df = price_df[
    price_df["price"].between(
        price_range[0],
        price_range[1],
    )
]

rarity_prices = (
    filtered_df.groupby("rarity")["price"]
    .mean()
    .sort_values(ascending=True)
)

col1, col2 = st.columns(2)

with col1:
    st.metric("Cards na faixa", len(filtered_df))

with col2:
    average_price = (
        filtered_df["price"].mean()
        if not filtered_df.empty
        else 0
    )

    st.metric(
        "Preço médio",
        f"{average_price:.2f}" if not filtered_df.empty else "—",
    )

if rarity_prices.empty:
    st.warning(
        "Nenhum card encontrado nessa faixa de preço. "
        "Ajuste o filtro para visualizar o gráfico."
    )
else:
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(
        rarity_prices.index.astype(str),
        rarity_prices.values,
        color="#7C4DFF",
    )

    ax.set_title("Preço médio por raridade")
    ax.set_xlabel("Raridade")
    ax.set_ylabel("Preço médio")
    ax.tick_params(axis="x", rotation=90)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with st.expander("Ver tabela de preços"):
    st.dataframe(
        filtered_df.sort_values("price", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

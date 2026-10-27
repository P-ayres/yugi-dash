
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Raridade dos cards",
    page_icon="src/yugi_dash/app/data/icon.png",
    layout="wide",
)


@st.cache_data
def load_data():
    return pd.read_csv("src/yugi_dash/app/data/yugioh.csv")


df = load_data()

st.markdown("## 🀆 Distribuição de Raridade dos Cards 🀆")
st.write(
    "Selecione o tipo de card para visualizar os cards daquela raridade."
)
st.markdown(
    "```O gráfico de barras mostra a quantidade de cards por raridade para o tipo selecionado, " \
    "selecionar uma raridade no seletor exibirá a quantidade de cards daquela raridade e uma tabela com os cards correspondentes.```"
)


type_options = sorted(df["type"].dropna().unique().tolist())

if not type_options:
    st.warning("Nenhum tipo de card encontrado.")
    st.stop()

selected_type = st.selectbox(
    "Tipo do Card",
    options=type_options,
)

filtered_df = df[df["type"] == selected_type].copy()

rarity_df = (
    filtered_df.dropna(subset=["rarity"])
    .groupby("rarity")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

col_chart, col_selector = st.columns([3, 1])

with col_chart:
    fig = px.bar(
        rarity_df,
        x="rarity",
        y="count",
        title=f"Distribuição de Raridade - {selected_type}",
        labels={
            "rarity": "Raridade",
            "count": "Quantidade de cards",
        },
        color_discrete_sequence=["#7C4DFF"],
    )

    st.plotly_chart(fig, use_container_width=True)

with col_selector:
    st.subheader("Filtro de raridade")

    selected_rarity = st.selectbox(
        "Selecione a raridade",
        options=rarity_df["rarity"].tolist(),
    )

    rarity_count = rarity_df.loc[
        rarity_df["rarity"] == selected_rarity, "count"
    ].iloc[0]

    st.metric("Quantidade de cards", int(rarity_count))

st.markdown("---")
st.subheader(f"Cards — {selected_rarity}")

cards_df = filtered_df[
    filtered_df["rarity"] == selected_rarity].copy()

columns = [
    col for col in cards_df.columns
]

cards_df = cards_df[columns]

st.dataframe(
    cards_df,
    use_container_width=True,
    hide_index=True,
)

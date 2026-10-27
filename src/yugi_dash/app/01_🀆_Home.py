import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="src/yugi_dash/app/data/icon.png",
    layout="wide"
)

st.title("🀆 Bem vindo ao dashboard 🀆")
st.sidebar.success("Selecione uma página para visualizar os dados relacionados as cartas.")
st.markdown(
    """
    Este dashboard foi desenvolvido contendo dados para análise de dados relacionados a Yu-Gi-Oh! e suas cartas. 
    Este dash conteḿ um visualização sobre dados comuns em cartas de Yugi-oh, como raridade, preço, atributos e volatilidade.
    """
)

st.badge("Monstros, Magias e Armadilhas")

st.button("``` Que slifer não te encontre ```", on_click=lambda: st.write("``` Mas o Faraó sim ```"))
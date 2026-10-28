from pathlib import Path
import streamlit as st
import pandas as pd

@st.cache_data(show_spinner="Loading card data...")
def load_data() -> pd.DataFrame:
    path = Path(__file__).resolve().parents[1] / "data" / "yugioh.csv"
    return pd.read_csv(path)

df = load_data()
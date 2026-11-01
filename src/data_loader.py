import pandas as pd
import streamlit as st


@st.cache_data
def load_data(path="data/clean/dataset.csv"):
    """Lê o dataset tratado (gerado no notebooks/eda-com-downloads.ipynb)."""
    df = pd.read_csv(path, parse_dates=["posting_date"])
    # mantém a ordem das faixas nos gráficos
    df["faixa_salarial"] = pd.Categorical(
        df["faixa_salarial"],
        categories=["50-100 mil", "100-150 mil", "150-200 mil", "200-250 mil"],
        ordered=True,
    )
    return df

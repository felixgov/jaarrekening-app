import streamlit as st
import pandas as pd

st.title("Jaarrekening Extractor v1")

st.write("Upload een jaarrekening (PDF)")

uploaded_file = st.file_uploader("Kies een PDF", type="pdf")

# vaste lijst van posten (basisversie)
schema = [
    "Omzet",
    "EBITDA",
    "EBIT",
    "Nettowinst",
    "Totale activa",
    "Eigen vermogen",
    "Totale schuld",
    "Cash",
    "Current assets",
    "Current liabilities",
    "CAPEX",
    "Afschrijvingen",
    "Interest expense",
    "Belastingen"
]

if uploaded_file:
    st.success("PDF geüpload")

    # placeholder output (v1)
    data = []
    for item in schema:
        data.append({
            "Post": item,
            "Gevonden": "Nee",
            "Waarde huidig jaar": "",
            "Waarde vorig jaar": ""
        })

    df = pd.DataFrame(data)

    st.subheader("Output")
    st.dataframe(df)

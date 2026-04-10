import streamlit as st
import pandas as pd
import pdfplumber

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

    import pdfplumber

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    data = []

    for item in schema:
        if item.lower() in text.lower():
            gevonden = "Ja"
        else:
            gevonden = "Nee"

        data.append({
            "Post": item,
            "Gevonden": gevonden,
            "Waarde huidig jaar": "",
            "Waarde vorig jaar": ""
        })

    df = pd.DataFrame(data)

    st.subheader("Output")
    st.dataframe(df)

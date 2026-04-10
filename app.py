import re
import streamlit as st
import pandas as pd
import pdfplumber

st.title("Jaarrekening Extractor v1")
st.write("Upload een jaarrekening (PDF)")

uploaded_file = st.file_uploader("Kies een PDF", type="pdf")

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

def classify_tokens(line):
    import re

    tokens = line.split()

    codes = []
    words = []
    amounts = []

    for token in tokens:
        t = token.strip()

        # bedrag: minstens 1 duizendtalseparator of decimalen in financieel formaat
        if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", t):
            amounts.append(t)

        # code / rekeningnummer: korte numerieke code of vorm zoals 10/15 of 6.9
        elif re.fullmatch(r"\d+(?:[./]\d+)+", t) or re.fullmatch(r"\d{1,3}", t):
            codes.append(t)

        else:
            words.append(t)

    label = " ".join(words)

    return {
        "codes": codes,
        "label": label,
        "amounts": amounts
    }

if uploaded_file:
    st.success("PDF geüpload")

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            text += "\n"

    lines = text.split("\n")
    data = []

    for item in schema:
        gevonden = "Nee"
        waarde = ""

        for line in lines:
            if item.lower() in line.lower():
                gevonden = "Ja"

                numbers = re.findall(r"\d[\d\.,]*", line)
                st.write(item, "|", line, "|", numbers)
                if numbers:
                    waarde = numbers[-1]

                break

        data.append({
            "Post": item,
            "Gevonden": gevonden,
            "Waarde huidig jaar": waarde,
            "Waarde vorig jaar": ""
        })

    df = pd.DataFrame(data)

    st.subheader("Output")
    st.dataframe(df)

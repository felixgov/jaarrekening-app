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
    tokens = line.split()

    codes = []
    words = []
    amounts = []

    for token in tokens:
        t = token.strip()

        if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", t):
            amounts.append(t)
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
        huidig = ""
        vorig = ""

        for line in lines:
            if item.lower() in line.lower():
                gevonden = "Ja"

                parsed = classify_tokens(line)
                st.write(item, "|", parsed)

                amounts = parsed["amounts"]

                if len(amounts) >= 2:
                    huidig = amounts[0]
                    vorig = amounts[1]
                elif len(amounts) == 1:
                    huidig = amounts[0]
                    vorig = ""

                break

        data.append({
            "Post": item,
            "Gevonden": gevonden,
            "Waarde huidig jaar": huidig,
            "Waarde vorig jaar": vorig
        })

    df = pd.DataFrame(data)

    st.subheader("Output")
    st.dataframe(df)

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Debug Mode", layout="wide")
st.title("🛠️ Diagnostic Mode")

st.write("Let's see what the computer is actually reading from the CSV...")

try:
    # 1. Read the raw text of the file
    with open("itinerary.csv", "r", encoding="utf-8-sig") as f:
        raw_text = f.read()
    
    st.subheader("1. The Raw Text File:")
    st.text(raw_text)

    # 2. Let Pandas try to load it
    df = pd.read_csv("itinerary.csv", encoding="utf-8-sig")
    
    st.subheader("2. The Column Names Pandas Sees:")
    # This will print out exactly what it thinks the columns are named
    st.write(df.columns.tolist())

    st.subheader("3. The Data Table:")
    st.dataframe(df)

except Exception as e:
    st.error(f"Error reading the file: {e}")
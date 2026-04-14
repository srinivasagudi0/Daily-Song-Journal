import streamlit as st

st.title("Daily Song Journal")

st.set_page_config(page_title="Daily Song Journal", page_icon=":musical_note:", layout="wide")

st.sidebar.header("Mode")
st.sidebar.selectbox("Mode", ["Journal"])

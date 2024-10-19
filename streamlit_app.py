import streamlit as st

st.title("BGA Testimonios")

text_search = st.text_input("Busca testimonios por caso de uso", value="")
industry = st.selectbox("Industria", ["", "Agricultura", "Finanzas"])

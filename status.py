import streamlit as st
import pandas as pd

# Título da página
st.title('Leitura de Arquivo Excel')

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Lê o arquivo Excel e carrega os dados em um DataFrame pandas
    df = pd.read_excel(uploaded_file, engine='openpyxl')  # engine='openpyxl' para ler arquivos .xlsx

    # Exibe os dados na interface
    st.write("Dados do Excel:")
    st.dataframe(df)  # Exibe os dados em forma de dataframe

import streamlit as st
import pandas as pd
import pickle
import os

def main():
    st.title("Execução de Script Python com Leitura de Excel e Pickle")

    # Upload do arquivo Excel
    uploaded_excel = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"])

    if uploaded_excel is not None:
        # Salvar o arquivo carregado temporariamente
        with open("uploaded_excel.xlsx", "wb") as f:
            f.write(uploaded_excel.getbuffer())

        # Ler o arquivo Excel carregado
        try:
            df = pd.read_excel("uploaded_excel.xlsx")
            st.subheader("Dados do Excel Carregado:")
            st.dataframe(df)

            # Exemplo de processamento e salvamento de dados em pickle
            output_data = {"dados": df.to_dict()}  # Exemplo de dados que seriam salvos

            # Salvar os dados em um arquivo pickle
            with open("output_data.pkl", "wb") as f:
                pickle.dump(output_data, f)

            st.success("Dados processados e salvos com sucesso em 'output_data.pkl'")
        except Exception as e:
            st.error(f"Erro ao processar o arquivo Excel: {e}")

    # Verificar e exibir o arquivo pickle se existir
    if os.path.exists("output_data.pkl"):
        try:
            with open("output_data.pkl", "rb") as f:
                loaded_data = pickle.load(f)
            st.subheader("Dados do Arquivo Pickle:")
            st.write(loaded_data)
        except Exception as e:
            st.error(f"Não foi possível ler os dados do arquivo pickle: {e}")

if __name__ == "__main__":
    main()

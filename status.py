import streamlit as st
import pickle
import os
import pandas as pd

def main():
    st.title("Leitura de Arquivo .pkl no Streamlit")

    # Upload do arquivo .pkl
    uploaded_file = st.file_uploader("Escolha um arquivo .pkl", type=["pkl"])

    if uploaded_file is not None:
        # Salvar o arquivo carregado temporariamente
        with open("uploaded_data.pkl", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Verificar se o arquivo foi carregado
        if os.path.exists("uploaded_data.pkl"):
            try:
                # Ler os dados do arquivo .pkl
                with open("uploaded_data.pkl", "rb") as f:
                    loaded_data = pickle.load(f)

                st.subheader("Dados Carregados do Arquivo .pkl:")
                st.write(loaded_data)

                # Converter os dados carregados para um DataFrame do pandas, se for possível
                if isinstance(loaded_data, dict):
                    df = pd.DataFrame.from_dict(loaded_data)
                elif isinstance(loaded_data, list):
                    df = pd.DataFrame(loaded_data)
                else:
                    st.error("Formato de dados não suportado para conversão para DataFrame.")
                    return

                # Mostrar os dados na tela
                st.subheader("Dados em Formato de DataFrame:")
                st.write(df)

                # Botão para baixar os dados como arquivo Excel
                st.download_button(
                    label="Baixar dados como Excel",
                    data=df.to_excel(index=False, engine='openpyxl'),
                    file_name="dados_carregados.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            except Exception as e:
                st.error(f"Erro ao carregar o arquivo .pkl: {e}")

if __name__ == "__main__":
    main()

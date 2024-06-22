import streamlit as st
import pickle
import os

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

                # Exemplo de processamento dos dados carregados
                # Aqui você pode realizar qualquer operação desejada com os dados

            except Exception as e:
                st.error(f"Erro ao carregar o arquivo .pkl: {e}")

if __name__ == "__main__":
    main()

import streamlit as st
import pickle
import pandas as pd
import io
import tempfile
import os

def main():
    st.title("Leitura de Arquivo .pkl no Streamlit")

    # Upload do arquivo .pkl
    uploaded_file = st.file_uploader("Escolha um arquivo .pkl", type=["pkl"])

    if uploaded_file is not None:
        try:
            # Ler os dados do arquivo .pkl
            loaded_data = pickle.load(uploaded_file)

            # Tentar converter para DataFrame
            if isinstance(loaded_data, pd.DataFrame):
                df = loaded_data
            elif isinstance(loaded_data, dict):
                if all(isinstance(v, (list, dict)) for v in loaded_data.values()):
                    df = pd.DataFrame.from_dict(loaded_data, orient='index').T
                else:
                    df = pd.DataFrame([loaded_data])
            elif isinstance(loaded_data, list):
                if all(isinstance(item, dict) for item in loaded_data):
                    df = pd.DataFrame(loaded_data)
                else:
                    df = pd.DataFrame(loaded_data)
            else:
                st.error("Formato de dados não suportado para conversão para DataFrame.")
                return

            # Mostrar os dados na tela de forma responsiva
            st.subheader("Dados em Formato de DataFrame:")
            st.dataframe(df)

            # Função para salvar DataFrame como arquivo Excel e retornar o caminho do arquivo
            def save_excel(df):
                temp_dir = tempfile.mkdtemp()
                file_path = os.path.join(temp_dir, "dados_carregados.xlsx")
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                return file_path

            # Salvar o DataFrame como arquivo Excel
            file_path = save_excel(df)

            # Criar link para baixar o arquivo Excel
            st.markdown(f"[Baixar dados como Excel](file://{file_path})")

        except Exception as e:
            st.error(f"Erro ao carregar o arquivo .pkl: {e}")

if __name__ == "__main__":
    main()

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

    # Selecionar ação
    choice = st.selectbox('Escolha uma ação', ['Carregar e Mostrar Dados', 'Inserir Excel'])

    # Caminho para o arquivo Excel
    csv_file_excel = 'dados_carregados.xlsx'

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
                with pd.ExcelWriter(csv_file_excel, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                return csv_file_excel

            # Salvar o DataFrame como arquivo Excel se a opção for escolhida
            if choice == 'Inserir Excel':
                file_path = save_excel(df)
                st.success(f"Dados salvos como Excel em: {file_path}")

            # Mostrar os dados do arquivo Excel armazenado se a escolha for 'Inserir Excel' e o arquivo existir
            if choice == 'Inserir Excel' and os.path.exists(csv_file_excel):
                df_excel = pd.read_excel(csv_file_excel)
                if not df_excel.empty:
                    st.write('**Dados do Excel Armazenados:**')
                    st.write(df_excel)

        except Exception as e:
            st.error(f"Erro ao carregar o arquivo .pkl: {e}")

if __name__ == "__main__":
    main()

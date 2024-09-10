import streamlit as st
import pandas as pd
import base64
import os
import pickle
import tempfile

# Função para salvar dados em um arquivo Pickle
def save_data_to_pickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

# Função para carregar dados de um arquivo Pickle
def load_data_from_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def main():
    st.title("Leitura de Arquivo .pkl no Streamlit")

    # Nome do arquivo .pkl para armazenar os dados em um diretório temporário
    pickle_file = os.path.join(tempfile.gettempdir(), 'dados.pkl')

    # Sidebar com opções
    menu = ['Carregar Dados', 'Visualizar Dados']
    choice = st.sidebar.selectbox('Escolha uma opção', menu)

    # Opção para carregar dados do arquivo .pkl
    if choice == 'Carregar Dados':
        st.title('Carregar Dados de Arquivo .pkl')

        # Upload do arquivo .pkl
        uploaded_file = st.file_uploader("Escolha um arquivo .pkl para carregar", type=["pkl"])

        if uploaded_file is not None:
            try:
                # Ler os dados do arquivo .pkl
                loaded_data = pickle.load(uploaded_file)

                # Salvar os dados carregados em um arquivo .pkl localmente
                save_data_to_pickle(loaded_data, pickle_file)
                st.success(f'Dados carregados e salvos com sucesso em {pickle_file}')

            except Exception as e:
                st.error(f"Erro ao carregar o arquivo .pkl: {e}")

    # Opção para visualizar dados carregados
    elif choice == 'Visualizar Dados':
        st.title('Visualizar Dados Carregados')

        # Verifica se o arquivo .pkl existe antes de tentar carregar
        if os.path.exists(pickle_file):
            try:
                loaded_data = load_data_from_pickle(pickle_file)

                # Exibir os dados carregados
                if isinstance(loaded_data, pd.DataFrame):
                    st.write('**Dados carregados como DataFrame:**')
                    st.write(loaded_data)
                else:
                    st.write('**Dados carregados:**')
                    st.write(loaded_data)
            except Exception as e:
                st.error(f"Erro ao carregar o arquivo .pkl: {e}")
        else:
            st.write('Nenhum dado foi carregado ainda.')

if __name__ == "__main__":
    main()
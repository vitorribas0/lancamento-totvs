import streamlit as st
import pandas as pd
import base64
import os
import pickle

# Função para salvar dados em um arquivo Pickle
def save_data_to_pickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

# Função para carregar dados de um arquivo Pickle
def load_data_from_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def main():
    st.title("Armazenamento e Acesso de Dados")

    # Nome do arquivo para armazenar os dados
    pickle_file = 'dados.pkl'

    # Sidebar com opções
    menu = ['Inserir Dados', 'Visualizar Dados']
    choice = st.sidebar.selectbox('Escolha uma opção', menu)

    # Opção para inserir dados
    if choice == 'Inserir Dados':
        st.title('Inserir Dados')

        # Campos para entrada de dados (exemplo com DataFrame)
        st.write('Insira dados como um DataFrame:')
        data = pd.DataFrame({
            'Nome': ['Alice', 'Bob', 'Charlie'],
            'Idade': [25, 30, 35]
        })

        # Mostrar dados na tela
        st.write(data)

        # Botão para salvar dados em um arquivo Pickle
        if st.button('Salvar Dados'):
            save_data_to_pickle(data, pickle_file)
            st.success(f'Dados salvos com sucesso em {pickle_file}')

    # Opção para visualizar dados
    elif choice == 'Visualizar Dados':
        st.title('Visualizar Dados')

        # Verifica se o arquivo existe antes de tentar carregar
        if os.path.exists(pickle_file):
            loaded_data = load_data_from_pickle(pickle_file)

            # Exibir os dados carregados
            if isinstance(loaded_data, pd.DataFrame):
                st.write('**Dados carregados:**')
                st.write(loaded_data)
            else:
                st.write('Dados carregados:')
                st.write(loaded_data)
        else:
            st.write('Nenhum dado foi armazenado ainda.')

if __name__ == "__main__":
    main()

import streamlit as st
import subprocess
import pickle
import os
import uuid

def main():
    st.title("Execução de Script Python com Leitura de Excel")

    # Upload do arquivo Python
    uploaded_file = st.file_uploader("Escolha um arquivo Python", type=["py","ipynb"])

    if uploaded_file is not None:
        # Gerar um nome de arquivo único para evitar colisões
        unique_filename = f"uploaded_script_{uuid.uuid4()}.py"
        with open(unique_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Obter o diretório onde o script Python está localizado
        script_directory = os.path.dirname(os.path.abspath(unique_filename))
        os.chdir(script_directory)  # Definir o diretório de trabalho para o diretório do script

        # Executar o script carregado e capturar a saída
        try:
            result = subprocess.run(["python", unique_filename], capture_output=True, text=True)
        except Exception as e:
            st.subheader("Erro na execução do script:")
            st.error(e)
            return

        # Exibir a saída do script
        st.subheader("Saída do Script:")
        st.text(result.stdout)

        # Exibir erros, se houver
        if result.stderr:
            st.subheader("Erros:")
            st.text(result.stderr)

        # Ler os dados armazenados no arquivo pickle
        pickle_file_path = "output_data.pkl"  # Caminho do arquivo pickle no mesmo diretório do script
        if os.path.exists(pickle_file_path):
            try:
                with open(pickle_file_path, "rb") as f:
                    df = pickle.load(f)
                st.subheader("Dados do Excel:")
                st.dataframe(df)
            except Exception as e:
                st.write("Não foi possível ler os dados do Excel:", e)
        else:
            st.write(f"Arquivo '{pickle_file_path}' não encontrado.")

        # Remover o arquivo temporário
        os.remove(unique_filename)

if __name__ == "__main__":
    main()

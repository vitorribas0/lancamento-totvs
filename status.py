import streamlit as st
import subprocess
import pickle
import os
import uuid
import logging

# Configure o logging
logging.basicConfig(level=logging.DEBUG)

def main():
    st.title("Execução de Script Python com Leitura de Excel")

    # Upload do arquivo Python
    uploaded_file = st.file_uploader("Escolha um arquivo Python", type=["py","ipynb"])

    if uploaded_file is not None:
        # Gerar um nome de arquivo único para evitar colisões
        unique_filename = f"uploaded_script_{uuid.uuid4()}.py"
        with open(unique_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        logging.debug(f"Arquivo Python carregado: {unique_filename}")

        # Executar o script carregado e capturar a saída
        try:
            result = subprocess.run(["python", unique_filename], capture_output=True, text=True)
            logging.debug("Script executado com sucesso.")
        except Exception as e:
            st.subheader("Erro na execução do script:")
            st.error(e)
            logging.error(f"Erro na execução do script: {e}")
            return

        # Exibir a saída do script
        st.subheader("Saída do Script:")
        st.text(result.stdout)

        # Exibir erros, se houver
        if result.stderr:
            st.subheader("Erros:")
            st.text(result.stderr)

        # Ler os dados armazenados no arquivo pickle
        pickle_file_path = "output_data.pkl"  # Caminho do arquivo pickle na máquina local
        if os.path.exists(pickle_file_path):
            try:
                with open(pickle_file_path, "rb") as f:
                    df = pickle.load(f)
                st.subheader("Dados do Excel:")
                st.dataframe(df)
            except Exception as e:
                st.write("Não foi possível ler os dados do Excel:", e)
                logging.error(f"Erro ao ler os dados do Excel: {e}")
        else:
            st.write(f"Arquivo '{pickle_file_path}' não encontrado.")
            logging.error(f"Arquivo '{pickle_file_path}' não encontrado.")

        # Remover o arquivo temporário
        os.remove(unique_filename)

if __name__ == "__main__":
    main()

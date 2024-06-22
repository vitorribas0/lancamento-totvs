import streamlit as st
import subprocess
import pickle


def main():
    st.title("Execução de Script Python com Leitura de Excel")

    # Upload do arquivo Python
    uploaded_file = st.file_uploader("Escolha um arquivo Python", type=["py","ipynb"])

    if uploaded_file is not None:
        # Salvar o arquivo carregado
        with open("uploaded_script.py", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Executar o script carregado e capturar a saída
        result = subprocess.run(["python", "uploaded_script.py"], capture_output=True, text=True)

        # Exibir a saída do script
        st.subheader("Saída do Script:")
        st.text(result.stdout)

        # Exibir erros, se houver
        if result.stderr:
            st.subheader("Erros:")
            st.text(result.stderr)

        # Ler os dados armazenados no arquivo pickle
        try:
            with open("output_data.pkl", "rb") as f:
                df = pickle.load(f)
            st.subheader("Dados do Excel:")
            st.dataframe(df)
        except Exception as e:
            st.write("Não foi possível ler os dados do Excel:", e)


if __name__ == "__main__":
    main()

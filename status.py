import streamlit as st
import subprocess
import nbformat
from nbconvert import PythonExporter
import pickle
import os
import sys

def install_dependencies():
    dependencies = ["pandas", "openpyxl", "nbconvert", "nbformat"]
    for dependency in dependencies:
        subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])

def convert_ipynb_to_py(ipynb_path, py_path):
    try:
        with open(ipynb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        exporter = PythonExporter()
        script, _ = exporter.from_notebook_node(nb)
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(script)
    except Exception as e:
        st.error(f"Erro ao converter o notebook: {e}")
        return False
    return True

def main():
    st.title("Execução de Notebook Jupyter com Leitura de Excel")

    # Upload do arquivo Notebook
    uploaded_file = st.file_uploader("Escolha um arquivo Jupyter Notebook", type=["ipynb"])

    if uploaded_file is not None:
        # Salvar o arquivo carregado
        ipynb_path = "uploaded_notebook.ipynb"
        py_path = "uploaded_script.py"
        with open(ipynb_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Converter o Notebook para script Python
        if not convert_ipynb_to_py(ipynb_path, py_path):
            st.stop()  # Se a conversão falhar, parar a execução
        
        # Instalar dependências necessárias
        install_dependencies()
        
        # Executar o script Python gerado e capturar a saída
        result = subprocess.run(["python", py_path], capture_output=True, text=True)
        
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
        except FileNotFoundError:
            st.write("Não foi possível ler os dados do Excel: arquivo 'output_data.pkl' não encontrado.")
        except Exception as e:
            st.write("Ocorreu um erro ao ler os dados do Excel:", e)

        # Limpar arquivos temporários
        os.remove(ipynb_path)
        os.remove(py_path)

if __name__ == "__main__":
    main()

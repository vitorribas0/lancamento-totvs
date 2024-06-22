import streamlit as st
import pickle
import pandas as pd
import io

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

            # Função para converter DataFrame para bytes de Excel
            def to_excel_bytes(df):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                return output.getvalue()

            # Botão para baixar os dados como arquivo Excel
            st.download_button(
                label="Baixar dados como Excel",
                data=to_excel_bytes(df),
                file_name="dados_carregados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"Erro ao carregar o arquivo .pkl: {e}")

        st.write(df)

if __name__ == "__main__":
    main()

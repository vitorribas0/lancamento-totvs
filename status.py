import streamlit as st
import pickle
import pandas as pd
import base64

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

            # Função para converter DataFrame para Excel em Base64
            def df_to_excel_base64(df):
                output = io.BytesIO()
                writer = pd.ExcelWriter(output, engine='openpyxl')
                df.to_excel(writer, index=False)
                writer.save()
                excel_data = output.getvalue()
                return excel_data

            # Converter DataFrame para Excel em Base64
            excel_data = df_to_excel_base64(df)

            # Codificar o Excel em Base64
            b64 = base64.b64encode(excel_data).decode()

            # Gerar link para download
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="dados.xlsx">Baixar Excel</a>'
            st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erro ao carregar o arquivo .pkl: {e}")

if __name__ == "__main__":
    main()

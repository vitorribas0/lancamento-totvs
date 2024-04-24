import pandas as pd
import streamlit as st
import os
import tempfile

# Nome da sua empresa
nome_empresa = "Indev Ribas"

# Adicionando um espaço em branco para mover o título para cima
st.sidebar.text("")

# Adicionando o nome da empresa na barra lateral
st.sidebar.title(nome_empresa)


def main():
    st.title("Processamento de Arquivos Excel")

    st.header("Upload de Arquivos")
    uploaded_danfe_files = st.file_uploader("Upload dos arquivos DANFE", accept_multiple_files=True)
    uploaded_notas_milhao_files = st.file_uploader("Upload dos arquivos Nota Milhão", accept_multiple_files=True)
    uploaded_totvs_file = st.file_uploader("Upload do arquivo Totvs")

    if uploaded_danfe_files and uploaded_notas_milhao_files and uploaded_totvs_file:
        dfs_danfe = []
        with tempfile.TemporaryDirectory() as temp_dir:
            for uploaded_file in uploaded_danfe_files:
                with open(os.path.join(temp_dir, uploaded_file.name), 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                df = pd.read_excel(os.path.join(temp_dir, uploaded_file.name), skiprows=2)
                df = df.dropna(axis=1, how='all')
                dfs_danfe.append(df)
        df_concatenado_danfe = pd.concat(dfs_danfe, ignore_index=True)
        df_concatenado_danfe = df_concatenado_danfe[
            ['Num NFe', 'Razão Soc. Emit', 'Valor', 'Data Emissão', 'CNPJ Dest']]
        df_concatenado_danfe['tipo'] = 'nf_produto'

        dataframes = []
        with tempfile.TemporaryDirectory() as temp_dir:
            for uploaded_file in uploaded_notas_milhao_files:
                with open(os.path.join(temp_dir, uploaded_file.name), 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                df = pd.read_excel(os.path.join(temp_dir, uploaded_file.name))
                df = df.dropna(axis=1, how='all')
                dataframes.append(df)
        concatenado = pd.concat(dataframes, ignore_index=True)
        concatenado = concatenado.rename(columns={
            'Nº NFS-e': 'Num NFe',
            'Razão Social do Prestador': 'Razão Soc. Emit',
            'Valor dos Serviços': 'Valor',
            'Data do Fato Gerador': 'Data Emissão',
            'CPF/CNPJ do Tomador': 'CNPJ Dest'
        })
        concatenado['Data Emissão'] = pd.to_datetime(concatenado['Data Emissão'])
        concatenado['Data Emissão'] = concatenado['Data Emissão'].dt.strftime('%d/%m/%Y')
        concatenado['tipo'] = 'nf_serviço'

        df_concatenado = pd.concat([df_concatenado_danfe, concatenado], ignore_index=True)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_totvs_path = os.path.join(temp_dir, "uploaded_totvs.xlsx")
            with open(temp_totvs_path, 'wb') as f:
                f.write(uploaded_totvs_file.getbuffer())
            df_totvs = pd.read_excel(temp_totvs_path, header=3)

        lançado = pd.merge(df_concatenado, df_totvs,
                           left_on=['Razão Soc. Emit', 'Valor'],
                           right_on=['RAZÃO SOCIAL', 'VALOR DA NF'],
                           how='left')

        lançado['DDT.PG.'] = lançado['DT.PG.'].dt.strftime('%d/%m/%Y')

        lançado = lançado[
            ['Num NFe', 'Razão Soc. Emit', 'Valor', 'Data Emissão', 'CNPJ Dest', 'FORNECEDOR', 'tipo', 'VALOR', 'NF','RAZÃO SOCIAL',
             'CENTRO DE RESPONSABILIDADE', 'DESCRIÇÃO APROPRIAÇÃO',
             'DT.PG.', 'OBSERVAÇÃO']]

        if not lançado.empty:
            st.header("Resultado do Processamento")
            st.write("Resultado final:")
            st.write(lançado.head())

            st.header("Download do Resultado")
            csv = lançado.to_csv(index=False)
            st.download_button(label="Download CSV", data=csv, file_name="resultado.csv", mime="text/csv")
        else:
            st.warning("Nenhum resultado para download.")


if __name__ == "__main__":
    main()

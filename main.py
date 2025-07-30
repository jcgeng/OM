import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar e exibir os arquivos
def carregar_planilha(upload):
    if upload is not None:
        if upload.name.endswith('.csv'):
            return pd.read_csv(upload)
        elif upload.name.endswith('.xlsx'):
            return pd.read_excel(upload)
        else:
            st.error("Formato de arquivo não suportado. Por favor, envie um arquivo .csv ou .xlsx")
            return None
    return None

# Configuração do Streamlit
st.title("Análise de Ordens de Manutenção e Apontamentos")

# Upload do arquivo
upload = st.file_uploader("Envie as planilhas de OMs e Apontamentos", type=["xlsx", "csv"], accept_multiple_files=True)

if upload:
    for file in upload:
        df = carregar_planilha(file)
        if df is not None:
            st.write(f"Exibindo dados do arquivo: {file.name}")
            st.dataframe(df)  # Exibe os dados no app
            
            # Criar gráfico (Exemplo: gráfico de barras)
            if "Cód. O. M" in df.columns:
                fig = px.bar(df, x="Cód. O. M", y="Hrs. Trabalhadas", title="Horas Trabalhadas por Ordem de Manutenção")
                st.plotly_chart(fig)  # Exibe o gráfico
        else:
            st.warning(f"Erro ao processar o arquivo {file.name}")

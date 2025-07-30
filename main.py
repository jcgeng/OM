import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from carregar_planilha import carregar_planilha
from padronizar_colunas import padronizar_coluna_cod_om, padronizar_coluna_hr_trabalhadas
from aplicar_filtros import aplicar_filtros

# Função para verificar se as colunas essenciais estão presentes
def verificar_colunas(df, colunas_necessarias):
    # Exibir as colunas para diagnóstico
    st.write("Colunas presentes na planilha:", df.columns.tolist())
    
    for col in colunas_necessarias:
        if col not in df.columns:
            st.error(f"A coluna '{col}' está faltando.")
            return False
    return True

# Função para unir as duas planilhas
def unir_planilhas(df_ordens, df_apontamentos):
    if "Cód. O. M." in df_ordens.columns and "Cód. O. M." in df_apontamentos.columns:
        return pd.merge(df_ordens, df_apontamentos, on="Cód. O. M.", how="left")
    else:
        st.error("A coluna 'Cód. O. M.' não está presente em ambas as planilhas.")
        return None

# Definir o primeiro dia do ano e a data atual
hoje = datetime.today()
primeiro_dia_ano = datetime(hoje.year, 1, 1)

# Configuração do Streamlit
st.title("Análise de Ordens de Manutenção e Apontamentos")

# Menu lateral (sidebar)
with st.sidebar:
    # Botão de envio de arquivos no topo
    st.header("Envio de Arquivos")
    upload = st.file_uploader("Envie as planilhas de Ordens de Manutenção e Apontamentos", type=["xlsx", "csv"], accept_multiple_files=True)

    st.header("Filtros de Análise")

    # Filtro de Tipo de Manutenção
    tipos_manutencao = st.selectbox("Tipo de Manutenção", ["", "Manutenção Preventiva", "Manutenção Corretiva", "Outros"])

    # Organizar os filtros de Data em uma linha
    col1, col2 = st.columns(2)

    with col1:
        # Filtro de Data de Cadastro
        data_cadastro_inicio = st.date_input("Data de Cadastro - Início", value=primeiro_dia_ano)
    with col2:
        # Filtro de Data de Cadastro
        data_cadastro_fim = st.date_input("Data de Cadastro - Fim", value=hoje)

    # Organizar os filtros de Data em uma linha
    col3, col4 = st.columns(2)

    with col3:
        # Filtro de Data de Conclusão
        data_conclusao_inicio = st.date_input("Data de Conclusão - Início", value=primeiro_dia_ano)
    with col4:
        # Filtro de Data de Conclusão
        data_conclusao_fim = st.date_input("Data de Conclusão - Fim", value=hoje)

if upload:
    # Carregar as duas planilhas
    if len(upload) == 2:
        df_ordens = carregar_planilha(upload[0])
        df_apontamentos = carregar_planilha(upload[1])

        if df_ordens is not None and df_apontamentos is not None:
            # Exibir colunas para diagnóstico
            st.write("Colunas da planilha de Ordens:", df_ordens.columns.tolist())
            st.write("Colunas da planilha de Apontamentos:", df_apontamentos.columns.tolist())
            
            # Padronizar as colunas para garantir consistência
            df_ordens = padronizar_coluna_cod_om(df_ordens)
            df_apontamentos = padronizar_coluna_cod_om(df_apontamentos)
            
            # Padronizar a coluna 'Hrs. Trabalhadas' apenas na planilha de Apontamentos
            df_apontamentos = padronizar_coluna_hr_trabalhadas(df_apontamentos)
            
            # Verificar se as colunas necessárias estão presentes
            if df_ordens is None or df_apontamentos is None:
                st.error("A coluna 'Cód. O. M.' ou 'Hrs. Trabalhadas' não foi encontrada em uma das planilhas.")
            else:
                # Verificar se as colunas necessárias estão presentes
                if verificar_colunas(df_ordens, ["Cód. O. M."]) and verificar_colunas(df_apontamentos, ["Cód. O. M.", "Hrs. Trabalhadas"]):
                    # Unir as planilhas
                    df_unido = unir_planilhas(df_ordens, df_apontamentos)
                    
                    if df_unido is not None:
                        # Filtro de Equipe (Usando a coluna 'Equipe')
                        equipes = df_unido['Equipe'].dropna().unique()  # Garantir que só os valores existentes sejam filtrados
                        equipe = st.sidebar.multiselect("Equipe", equipes, default=equipes)
                        
                        # Filtro de Técnico (Usando a coluna 'Membro da Equipe')
                        tecnicos = df_unido['Membro da Equipe'].dropna().unique()  # Garantir que só os valores existentes sejam filtrados
                        tecnico = st.sidebar.multiselect("Técnico", tecnicos, default=tecnicos)
                        
                        # Aplicar filtros aos dados
                        df_filtrado = aplicar_filtros(df_unido, data_cadastro_inicio, data_cadastro_fim, data_conclusao_inicio, data_conclusao_fim, tipos_manutencao, equipe, tecnico)
                        
                        # Diagnóstico: Exibir o tamanho do DataFrame após os filtros
                        st.write(f"Dados após aplicação dos filtros: {df_filtrado.shape[0]} registros.")
                        
                        # Exibir dados filtrados
                        st.write(f"Dados Filtrados:")
                        st.dataframe(df_filtrado)
                        
                        # Criar gráfico de barras (Exemplo)
                        if not df_filtrado.empty:
                            fig = px.bar(df_filtrado, x="Cód. O. M.", y="Hrs. Trabalhadas", title="Horas Trabalhadas por Ordem de Manutenção")
                            st.plotly_chart(fig)
                        else:
                            st.warning("Nenhum dado encontrado para os filtros aplicados.")
    else:
        st.warning("Por favor, envie exatamente duas planilhas.")

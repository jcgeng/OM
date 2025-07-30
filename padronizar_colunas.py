import pandas as pd
import streamlit as st

def padronizar_coluna_cod_om(df):
    df.columns = df.columns.str.strip()  # Remove espaços extras nos nomes das colunas
    # Variações possíveis de 'Cód. O. M.'
    colunas_possiveis = ['Cód. O. M.', 'cód. o.m', 'Cód O.M', 'Cód O.M.', 'Cód. O.M.', 'Cód. O. M']
    for coluna in colunas_possiveis:
        if coluna in df.columns:
            df = df.rename(columns={coluna: 'Cód. O. M.'})
            return df
    st.error("A coluna 'Cód. O. M.' não foi encontrada na planilha.")
    return df  # Retorna o DataFrame sem modificações, se a coluna não for encontrada

def padronizar_coluna_hr_trabalhadas(df):
    df.columns = df.columns.str.strip()  # Remove espaços extras nos nomes das colunas
    # Verifica se a coluna 'Hrs. Trabalhadas' está presente
    if 'Hrs. Trabalhadas' in df.columns:
        return df  # Se a coluna já está com o nome correto, apenas retorna o dataframe
    # Variações possíveis de 'Hrs. Trabalhadas'
    colunas_possiveis = ['Horas Trabalhadas', 'Horas Trabladas', 'Horas', 'Hr. Trabalhadas', 'Horas Trabalhada']
    for coluna in colunas_possiveis:
        if coluna in df.columns:
            df = df.rename(columns={coluna: 'Hrs. Trabalhadas'})
            return df
    st.error("A coluna 'Hrs. Trabalhadas' não foi encontrada na planilha de Apontamentos.")
    return df  # Retorna o DataFrame sem modificações, se a coluna não for encontrada

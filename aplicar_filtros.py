import pandas as pd

def aplicar_filtros(df, data_cadastro_inicio, data_cadastro_fim, data_conclusao_inicio, data_conclusao_fim, tipo_manutencao, equipe, tecnico):
    # Garantir que a coluna 'Dt. Cadastro O.M' e 'Dt. Conclusão' sejam do tipo datetime
    df['Dt. Cadastro O.M'] = pd.to_datetime(df['Dt. Cadastro O.M'], errors='coerce')
    df['Dt. Conclusão'] = pd.to_datetime(df['Dt. Conclusão'], errors='coerce')
    
    # Converter as datas de entrada para o tipo datetime para comparação
    data_cadastro_inicio = pd.to_datetime(data_cadastro_inicio)
    data_cadastro_fim = pd.to_datetime(data_cadastro_fim)
    data_conclusao_inicio = pd.to_datetime(data_conclusao_inicio)
    data_conclusao_fim = pd.to_datetime(data_conclusao_fim)
    
    # Filtro de Data de Cadastro
    if data_cadastro_inicio and data_cadastro_fim:
        df = df[(df['Dt. Cadastro O.M'] >= data_cadastro_inicio) & (df['Dt. Cadastro O.M'] <= data_cadastro_fim)]
    
    # Filtro de Data de Conclusão
    if data_conclusao_inicio and data_conclusao_fim:
        df = df[(df['Dt. Conclusão'] >= data_conclusao_inicio) & (df['Dt. Conclusão'] <= data_conclusao_fim)]
    
    # Filtro de Tipo de Manutenção
    if tipo_manutencao:
        df = df[df['Tipo de O.M.'] == tipo_manutencao]
    
    # Filtro de Equipe
    if equipe:
        df = df[df['Equipe'].isin(equipe)]
    
    # Filtro de Técnico
    if tecnico:
        df = df[df['Membro da Equipe'].isin(tecnico)]
    
    return df

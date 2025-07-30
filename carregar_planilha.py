import pandas as pd

def carregar_planilha(upload):
    if upload is not None:
        if upload.name.endswith('.csv'):
            return pd.read_csv(upload)
        elif upload.name.endswith('.xlsx'):
            return pd.read_excel(upload, skiprows=2)
        else:
            return None
    return None

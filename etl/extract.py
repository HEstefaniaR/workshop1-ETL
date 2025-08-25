import pandas as pd

def extract(file_path):
    df = pd.read_csv(file_path, sep=';')
    print(f'Datos extraidos correctamente')

    return df

import pandas as pd
import csv
from urllib.request import urlopen
import requests
from datetime import datetime
from pathlib import Path

#keys e cidade e pais
api_key = 'c8356f4a0dba2e49ae6bcc2747ea6b25'
cidade = 'Porto Alegre'
cidade01 = 'Canela'
cidade02 = 'Capão da Canoa'
pais = 'br'
url = f'http://api.openweathermap.org/data/2.5/forecast?q={cidade},{pais}&appid={api_key}&units=metric'
url1 = f'http://api.openweathermap.org/data/2.5/forecast?q={cidade01},{pais}&appid={api_key}&units=metric'
url2 = f'http://api.openweathermap.org/data/2.5/forecast?q={cidade02},{pais}&appid={api_key}&units=metric'


# request em json
response = requests.get(url)
response01 = requests.get(url1)
response02 = requests.get(url2)

# Verifique se os dados foram recebidos corretamente   

data = response.json()
data01 = response01.json()
data02 = response02.json()

#criar um df
df = pd.DataFrame()
df01 = pd.DataFrame()
df02 = pd.DataFrame()


# Verifique se os dados foram recebidos corretamente
if response.status_code == 200 and 'list' in data:
    # Transforme os dados em um DataFrame
    forecast_list = data['list']
    df = pd.DataFrame(forecast_list)
    
    # Extrair informações importantes
    df['date'] = pd.to_datetime(df['dt'], unit='s')
    df['temperature'] = df['main'].apply(lambda x: x['temp'])
    df['city'] = cidade
    
    # Teste de resultados
    print('Dados de Porto Alegre extraídos com sucesso!')

    # Salvar em CSV
    df.to_csv('portoalegre.csv', index=False)
    
else:
    print("Erro ao obter os dados de Porto Alegre:", data.get('message', 'Erro desconhecido'))

if response01.status_code == 200 and 'list' in data01:
    forecast_list = data01['list']
    df01 = pd.DataFrame(forecast_list)
    df01['date'] = pd.to_datetime(df01['dt'], unit='s')
    df01['temperature'] = df01['main'].apply(lambda x: x['temp'])
    df01['city'] = cidade01
    
    print('Dados de Canela extraídos com sucesso!')

    # Salvar em CSV
    df01.to_csv('canela.csv', index=False)
    
else:
    print("Erro ao obter os dados de Canela:", data01.get('message', 'Erro desconhecido'))

if response02.status_code == 200 and 'list' in data02:
    forecast_list = data02['list']
    df02 = pd.DataFrame(forecast_list)
    df02['date'] = pd.to_datetime(df02['dt'], unit='s')
    df02['temperature'] = df02['main'].apply(lambda x: x['temp'])
    df02['city'] = cidade02
    
    print('Dados de Capão da Canoa extraídos com sucesso!')

    # Salvar em CSV
    df02.to_csv('capaodacanoa.csv', index=False)
    
else:
    print("Erro ao obter os dados de Capão da Canoa:", data02.get('message', 'Erro desconhecido'))


current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()


portoalegre = current_dir / 'portoalegre.csv'
capaodacanoa = current_dir / 'capaodacanoa.csv'
canela = current_dir / 'canela.csv'
historico = current_dir / 'base_historico.csv'


# Ler os arquivos CSV
df1 = pd.read_csv(portoalegre)
df2 = pd.read_csv(capaodacanoa)
df3 = pd.read_csv(canela)
df4 = pd.read_csv(historico)


# Concatenar os DataFrames
df_concatenado = pd.concat([df, df1, df2,df4], ignore_index=True)

# Remover os dados duplicados
df_sem_duplicatas = df_concatenado.drop_duplicates()

# Salvar o DataFrame resultante em um novo arquivo CSV
df_sem_duplicatas.to_csv('base_historico.csv', index=False)

print("Arquivos concatenados e duplicatas removidas com sucesso!")

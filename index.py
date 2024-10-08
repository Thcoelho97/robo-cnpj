import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re

# Configurar o driver do Selenium
driver_path = '/opt/homebrew/bin/chromedriver'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

# Carregar a planilha (agora no formato .xlsx) e remover espaços extras
df = pd.read_excel('/Users/thiagocoelho/Downloads/companies.xlsx', engine='openpyxl')
df['Company name'] = df['Company name'].str.strip()  # Limpar espaços extras

# Definir coluna para armazenar o resultado
df['CNPJ'] = None  # Inicializar a coluna com valores vazios

# Função para extrair o CNPJ de uma string usando regex
def extrair_cnpj(texto):
    # Regex para encontrar CNPJ no formato 99.999.999/9999-99
    padrao_cnpj = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
    
    match = re.search(padrao_cnpj, texto)
    if match:
        return match.group(0)  # Retorna o CNPJ encontrado
    return None  # Retorna None se não encontrar CNPJ

# Iterar sobre as linhas da planilha
for index, row in df.iterrows():
    nome_empresa = str(row['Company name']).strip()  # Remove espaços
    print(f'Pesquisando CNPJ para: {nome_empresa}')  # Exibe o nome da empresa sendo processada
    
    # Acessar o Google e realizar a pesquisa
    driver.get('https://www.google.com')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(f'{nome_empresa} CNPJ')
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)  # Esperar a página carregar

    # Coletar o conteúdo da página de resultados
    try:
        resultado = driver.find_element(By.CSS_SELECTOR, 'div.g').text  # Mude o seletor conforme necessário
        cnpj_encontrado = extrair_cnpj(resultado)
        
        if cnpj_encontrado:
            df.at[index, 'CNPJ'] = cnpj_encontrado
            print(f'CNPJ encontrado: {cnpj_encontrado}')
        else:
            df.at[index, 'CNPJ'] = 'CNPJ não encontrado'
            print(f'CNPJ não encontrado para: {nome_empresa}')
    
    except Exception as e:
        df.at[index, 'CNPJ'] = 'Erro ou Não Encontrado'
        print(f'Erro na pesquisa para {nome_empresa}: {e}')

# Fechar o navegador
driver.quit()

# Salvar os resultados em uma nova planilha
df.to_excel('/Users/thiagocoelho/Documents/companies_resultados.xlsx', index=False)
print("Pesquisa concluída e salva em companies_resultados.xlsx")
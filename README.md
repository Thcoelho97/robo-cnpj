# robo-cnpj
Um robo para pegar as empresas somente pelo nome em uma planilha e compilar os cnpjs buscados no google

certifique-se de instalar o webdriver da sua preferencia, o pandas o openpyxl e o selenium

Primeiro passo

pip install pandas selenium openpyxl

Segundo passo

Para o Selenium, você precisa de um WebDriver para o navegador que deseja usar (como Chrome ou Firefox).

from selenium import webdriver

driver_path = '/usr/local/bin/chromedriver'  # Este é o caminho do seu WebDriver

driver = webdriver.Chrome(executable_path=driver_path)
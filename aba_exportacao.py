import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

## Processamento

# URL corrigida (sem subopcao)
dominio = "http://vitibrasil.cnpuv.embrapa.br/"

url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06'

# Faz a requisição
response = requests.get(url)
response.encoding = 'utf-8'  # Sim, isso é necessário para acentuação

# Criar um dicionário para armazenar os itens e seus respectivos caminhos
opcoes_pg_producao = {}

# Verifica sucesso
if response.status_code == 200:
    print("Página acessada com sucesso!")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todos os botões do formulário
    buttons = soup.find_all('button', class_='btn_sopt')

    # Iterar sobre os botões para extrair o nome e o valor do atributo 'value'
    for button in buttons:
        item_name = button.text.strip()  # Nome do item
        subopcao_value = button['value']  # Caminho (valor do atributo 'value')
        
        # Armazenar no dicionário
        opcoes_pg_producao[item_name] = subopcao_value

else:
    print(f"Erro: {response.status_code}")

print(opcoes_pg_producao)

# # # --------------------------------------------------------------------------
anos = 2023

for key, value in opcoes_pg_producao.items():
    print(key, value)

    aux = f'index.php?ano={anos}&opcao=opt_06&subopcao={value}'

    url_completa = dominio + aux

    # Faz a requisição
    response_item = requests.get(url_completa)
    response_item.encoding = 'utf-8'  # Sim, isso é necessário para acentuação

    # Verifica sucesso
    if response.status_code == 200:
        soup_subopt = BeautifulSoup(response_item.text, 'html.parser')

        # Localiza a tabela
        tabela = soup_subopt.find('table', class_='tb_base tb_dados')

        # Extrai os cabeçalhos da tabela
        thead = tabela.find('thead')
        colunas = [th.get_text(strip=True) for th in thead.find_all('th')]

        # Extrai os dados do corpo da tabela
        linhas = []
        for linha in tabela.tbody.find_all('tr'):
            valores = []
            for i, td in enumerate(linha.find_all('td')):
                texto = td.get_text(strip=True).replace('.', '').replace(',', '')
                if texto == '-':
                    valores.append(None)
                elif i > 0:  # Quantidade e valor
                    valores.append(int(texto))
                else:
                    valores.append(texto)
            linhas.append(valores)

        # Cria o DataFrame
        df = pd.DataFrame(linhas, columns=colunas)

        # Exporta para JSON no formato de lista de registros
        df.to_json(f"json_exportacao_{key}_{anos}.json", orient='records', force_ascii=False, indent=2)

        print(f"JSON salvo como 'importacao_suco_uva_{anos}.json'")

   
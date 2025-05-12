import pandas as pd
from bs4 import BeautifulSoup
import requests
from io import StringIO
import json

 #### Produção
dominio = 'http://vitibrasil.cnpuv.embrapa.br/'

# 1979 a 2023
ano = 2023

complemento = f"index.php?ano={ano}&opcao=opt_04"



response = requests.get(dominio+complemento)

# Garante correta leitura de caracteres acentuados
response.encoding = 'utf-8'


# Verifica se a página foi acessada com sucesso
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    tabela = soup.find('table', class_='tb_base tb_dados')

    dados_json = {}
    categoria_atual = None

    for row in tabela.find('tbody').find_all('tr'):
        cols = [col.text.strip() for col in row.find_all('td')]
        if len(cols) != 2:
            continue
        nome, quantidade = cols

        # Verifica se é categoria principal
        if 'tb_item' in row.find('td')['class']:
            categoria_atual = nome
            dados_json[categoria_atual] = {'total': quantidade}

        # Verifica se é subitem
        elif 'tb_subitem' in row.find('td')['class']:
            if categoria_atual:
                dados_json[categoria_atual][nome] = quantidade

    # Adiciona o total geral da tabela (rodapé)
    tfoot = tabela.find('tfoot')
    if tfoot:
        total_row = [td.text.strip() for td in tfoot.find_all('td')]
        if len(total_row) == 2:
            dados_json['TOTAL GERAL'] = {total_row[0]: total_row[1]}

    # Salva o JSON estruturado
    json_file = f"tabela_comercialização_{ano}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(dados_json, f, ensure_ascii=False, indent=2)

    print(f"JSON estruturado salvo como: {json_file}")

else:
    print(f"Erro ao acessar a página. Código HTTP: {response.status_code}")

#     # Encontra a tabela de dados
#     tabela = soup.find('table', class_='tb_base tb_dados')

#     # Coleta os dados
#     dados = []
#     for linha in tabela.find_all('tr'):
#         colunas = linha.find_all(['td', 'th'])
#         dados.append([col.text.strip() for col in colunas])

#     # Cria um DataFrame
#     df = pd.DataFrame(dados[1:], columns=dados[0])

#     # Mostra as 5 primeiras linhas
#     print(df.head())
    
#     # Salva como CSV
#     df.to_csv('producao_vinhos_2021.csv', index=False, encoding='utf-8-sig')

#     # Salva como JSON
#     json_file = f"tabela_producao_uva_vinho_{ano}.json"
#     df.to_json(json_file, orient='records', force_ascii=False, indent=2)
# else:
#     print(f"Erro ao acessar a página: {response.status_code}")


import requests
from bs4 import BeautifulSoup
import json

## Processamento

# URL corrigida (sem subopcao)
dominio = "http://vitibrasil.cnpuv.embrapa.br/"

url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2022&opcao=opt_03'

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

    # txt_file = "html.txt"
    # with open(txt_file, 'w', encoding='utf-8') as f:
    #     f.write(str(soup))  


else:
    print(f"Erro: {response.status_code}")


print(opcoes_pg_producao)

# # --------------------------------------------------------------------------
# anos = 2023

# #http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2022&opcao=opt_03&subopcao=subopt_02
# for key, value in opcoes_pg_producao.items():
#     print(key, value)

#     aux = f'index.php?ano={anos}&opcao=opt_03&subopcao={value}'

#     url_completa = dominio + aux

#     # Faz a requisição
#     response_item = requests.get(url_completa)
#     response_item.encoding = 'utf-8'  # Sim, isso é necessário para acentuação

#     # Verifica sucesso
#     if response.status_code == 200:
#         soup_subopt = BeautifulSoup(response_item.text, 'html.parser')

#         # print(key, value)

#         tabela = soup_subopt.find('table', class_='tb_base tb_dados')

#         dados_json = {}
#         categoria_atual = None

#         for row in tabela.find('tbody').find_all('tr'):
#             cols = [col.text.strip() for col in row.find_all('td')]
#             if len(cols) != 2:
#                 continue
#             nome, quantidade = cols

#             # Verifica se é categoria principal
#             if 'tb_item' in row.find('td')['class']:
#                 categoria_atual = nome
#                 dados_json[categoria_atual] = {'total': quantidade}

#             elif 'tb_subitem' in row.find('td')['class']:
#                 if categoria_atual:
#                     dados_json[categoria_atual][nome] = quantidade

#         # Adiciona o total geral da tabela (rodapé)
#         tfoot = tabela.find('tfoot')
#         if tfoot:
#             total_row = [td.text.strip() for td in tfoot.find_all('td')]
#             dados_json['TOTAL GERAL'] = {total_row[0]: total_row[1]}

#             # Salva o JSON hierárquico
#             json_file = f"tabela_{key}.json"
#             with open(json_file, 'w', encoding='utf-8') as f:
#                 json.dump(dados_json, f, ensure_ascii=False, indent=2)

#             print(f"JSON estruturado salvo como: {json_file}")

#         else:
#             print(f"Erro ao acessar a página. Código HTTP: {response.status_code}")

                # txt_file = f"html_{key}.txt"
                # with open(txt_file, 'w', encoding='utf-8') as f:
                #     f.write(str(soup_subopt))  


import pandas as pd
from bs4 import BeautifulSoup
import requests
from io import StringIO
import json


class GetEmbrapaData():

    def __init__(self):
        self.dominio = 'http://vitibrasil.cnpuv.embrapa.br/'
    

    def get_production_data(self, ano):
        try:
            complemento = f"index.php?ano={ano}&opcao=opt_02"

            # Faz a requisição para a página
            response = requests.get(self.dominio+complemento)

            # Garante a correta leitura de caracteres acentuados
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
                # json_file = f"dados_producao_{ano}.json"
                # with open(json_file, 'w', encoding='utf-8') as f:
                #     json.dump(dados_json, f, ensure_ascii=False, indent=2)

                # print(f"JSON estruturado salvo como: {json_file}")

            else:
                print(f"Erro ao acessar a página. Código HTTP: {response.status_code}")

            if len(dados_json) > 0:
                dados_json['ano'] = ano

            return dados_json
        
        except requests.exceptions.RequestException as e:
            return {"erro": f"Erro na requisição HTTP: {str(e)}"}
        
        except Exception as e:
            return {"erro": f"Erro inesperado: {str(e)}"}

    
      
    def get_exportation_data():
        pass

    def get_commercialization_data():
        pass

    def get_importation_data():
        pass

    def get_processing_data():
        pass
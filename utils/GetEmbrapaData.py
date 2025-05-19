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

                if len(dados_json) > 0:
                    dados_json['ano'] = ano

                return dados_json
            
            return {"erro": f"Erro ao acessar a página. Código HTTP: {response.status_code}"}

        except requests.exceptions.RequestException as e:
            return {"erro": f"Erro na requisição HTTP: {str(e)}"}
        
        except Exception as e:
            return {"erro": f"Erro inesperado: {str(e)}"}


    def get_processing_data(self, ano, opcao):
        try:
            if opcao == 'Viníferas':
                opcao = 'subopt_01'
            elif opcao == 'Americanas e híbridas': 
                opcao = 'subopt_02'
            elif opcao == 'Uvas de mesa':
                opcao = 'subopt_03'
            elif opcao == 'Sem classificação':
                opcao = 'subopt_04'


            aux = f'index.php?ano={ano}&opcao=opt_03&subopcao={opcao}'

            url_completa = self.dominio + aux

            # Faz a requisição
            response_item = requests.get(url_completa)
            response_item.encoding = 'utf-8'  # Sim, isso é necessário para acentuação

            # Verifica sucesso
            if response_item.status_code == 200:
                soup_subopt = BeautifulSoup(response_item.text, 'html.parser')

                # print(key, value)

                tabela = soup_subopt.find('table', class_='tb_base tb_dados')

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

                    elif 'tb_subitem' in row.find('td')['class']:
                        if categoria_atual:
                            dados_json[categoria_atual][nome] = quantidade

                # Adiciona o total geral da tabela (rodapé)
                tfoot = tabela.find('tfoot')
                if tfoot:
                    total_row = [td.text.strip() for td in tfoot.find_all('td')]
                    dados_json['TOTAL GERAL'] = {total_row[0]: total_row[1]}

                if len(dados_json) > 0:
                    dados_json['ano'] = ano

                return dados_json

            # Se não for 200, retorna erro
            return {"erro": f"Erro ao acessar a página. Código HTTP: {response_item.status_code}"}
        
        except requests.exceptions.RequestException as e:
            return {"erro": f"Erro na requisição HTTP: {str(e)}"}
        
        except Exception as e:
            return {"erro": f"Erro inesperado: {str(e)}"}
    
    def get_commercialization_data(self, ano):
        try:
            complemento = f"index.php?ano={ano}&opcao=opt_04"

            response = requests.get(self.dominio+complemento)
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

                if len(dados_json) > 0:
                    dados_json['ano'] = ano
                
                return dados_json
            
            # Se não for 200, retorna erro
            return {"erro": f"Erro ao acessar a página. Código HTTP: {response.status_code}"}
        
        except requests.exceptions.RequestException as e:
            return {"erro": f"Erro na requisição HTTP: {str(e)}"}
        
        except Exception as e:
            return {"erro": f"Erro inesperado: {str(e)}"}
    
    def get_importation_data(self, ano, opcao):
        try: 
            if opcao == 'Vinhos de mesa':
                opcao = 'subopt_01'
            elif opcao == 'Espumantes':
                opcao = 'subopt_02'
            elif opcao == 'Uvas frescas':
                opcao = 'subopt_03'
            elif opcao == 'Uvas passas':
                opcao = 'subopt_04'
            elif opcao == 'Suco de uva':
                opcao = 'subopt_05'

            aux = f'index.php?ano={ano}&opcao=opt_05&subopcao={opcao}'

            url_completa = self.dominio + aux

            # Faz a requisição
            response_item = requests.get(url_completa)
            response_item.encoding = 'utf-8'  # Sim, isso é necessário para acentuação

            # Verifica sucesso
            if response_item.status_code == 200:
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
                df = df.fillna(0)

            

                # Retorna o JSON diretamente
                json_data = df.to_dict(orient='records')
                print(json.dumps(json_data, ensure_ascii=False, indent=2))
            
                return json_data
        
            # Se não for 200, retorna erro
            return {"erro": f"Erro ao acessar a página. Código HTTP: {response_item.status_code}"}
            
        except requests.exceptions.RequestException as e:
            return {"erro": f"Erro na requisição HTTP: {str(e)}"}
        
        except Exception as e:
            return {"erro": f"Erro inesperado: {str(e)}"}
        


    def get_exportation_data(self, ano, opcao):
        try: 
            if opcao == 'Vinhos de mesa':
                opcao = 'subopt_01'
            elif opcao == 'Espumantes':
                opcao = 'subopt_02'
            elif opcao == 'Uvas frescas':
                opcao = 'subopt_03'
            elif opcao == 'Suco de uva':
                opcao = 'subopt_04'

            aux = f'index.php?ano={ano}&opcao=opt_06&subopcao={opcao}'

            url_completa = self.dominio + aux

            # Faz a requisição
            response_item = requests.get(url_completa)
            response_item.encoding = 'utf-8'  # Sim, isso é necessário para acentuação

            # Verifica sucesso
            if response_item.status_code == 200:
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
                df = df.fillna(0)

            
                # Retorna o JSON diretamente
                json_data = df.to_dict(orient='records')
                print(json.dumps(json_data, ensure_ascii=False, indent=2))
            
                return json_data
        
            # Se não for 200, retorna erro
            return {"erro": f"Erro ao acessar a página. Código HTTP: {response_item.status_code}"}
            
        except requests.exceptions.RequestException as e:
            return {"erro": f"Erro na requisição HTTP: {str(e)}"}
        
        except Exception as e:
            return {"erro": f"Erro inesperado: {str(e)}"}

    
    

   
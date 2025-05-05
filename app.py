from flask import Flask, request, jsonify
from flasgger import Swagger
import pandas as pd
import json

# Criação do app Flask e configuração do Swagger
app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': '5MLET - Fase 1',
    'uiversion': 3
}

swagger = Swagger(app)

@app.route('/soma', methods=['GET'])
def soma():
    """
    Soma dois números
    ---
    parameters:
      - name: a
        in: query
        type: number
        required: true
        description: Primeiro número a ser somado
      - name: b
        in: query
        type: number
        required: true
        description: Segundo número a ser somado
    responses:
      200:
        description: Resultado da soma
        schema:
          type: object
          properties:
            resultado:
              type: number
              example: 8.0
    """
    a = float(request.args.get('a'))
    b = float(request.args.get('b'))
    resultado = a + b
    return jsonify({'resultado': resultado})

@app.route('/multiplicacao', methods=['GET'])
def multiplicacao():
    """
    Multiplica dois números
    ---
    parameters:
      - name: x
        in: query
        type: number
        required: true
        description: Primeiro número a ser multiplicado
      - name: y
        in: query
        type: number
        required: true
        description: Segundo número a ser multiplicado
    responses:
      200:
        description: Resultado da multiplicação
        schema:
          type: object
          properties:
            resultado:
              type: number
              example: 15.0
    """
    x = float(request.args.get('x'))
    y = float(request.args.get('y'))
    resultado = x * y
    return jsonify({'resultado': resultado})

@app.route('/web', methods=['GET'])
def web():
    """
    Teste simples da API
    ---
    responses:
      200:
        description: Retorna uma resposta simples
        schema:
          type: object
          properties:
            resultado:
              type: string
              example: "ok"
    """
    return jsonify({'resultado': 'ok'})

@app.route('/web2', methods=['GET'])
def web2():
    """
    Teste simples da API
    ---
    parameters:
      - name: Domínio
        in: query
        type: string
        required: true
        default: "http://vitibrasil.cnpuv.embrapa.br/"
        description: Domínio do site. Exemplo - http://vitibrasil.cnpuv.embrapa.br/
      - name: Caminho
        in: query
        type: string
        required: true
        description: Caminho para uma parte específica de um site. Exemplo - index.php?opcao=opt_03

    responses:
      200:
        description: Retorna um dataframe.
        schema:
          type: object
          properties:
            resultado:
              type: string
              example: "ok"
    """

    # dominio = str(request.args.get('Dominio', default='http://vitibrasil.cnpuv.embrapa.br/'))
    # caminho = str(request.args.get('Caminho'))
   
    # return jsonify({'resultado': 'ok'})

     # Criando um DataFrame de exemplo com pandas
    data = {
        'coluna1': ['valor1', 'valor2', 'valor3'],
        'coluna2': ['valorA', 'valorB', 'valorC']
    }
    df = pd.DataFrame(data)
    
    # Convertendo o DataFrame para JSON
    df_json = df.to_json(orient='records')  # 'records' cria uma lista de dicionários

    # Carregar a string JSON em uma lista de objetos
    df_json = json.loads(df_json)
    
    # Retornando o DataFrame como resposta JSON
    return jsonify({'resultado': 'ok', 'data': df_json})








if __name__ == '__main__':
    app.run(debug=True)
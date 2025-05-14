from flask import Flask, jsonify, request, redirect, render_template_string, url_for
from flasgger import Swagger
from utils.GetEmbrapaData import GetEmbrapaData

app = Flask(__name__)
swagger = Swagger(app)

# Página de login com formulário HTML básico
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aqui poderia validar usuário/senha, mas vamos direto redirecionar
        return redirect(url_for('flasgger.apidocs'))
    
    # HTML do formulário
    return render_template_string("""
    <!doctype html>
    <html>
    <head><title>Login</title></head>
    <body>
        <h2>Login</h2>
        <form method="post">
            <label>Usuário:</label><br>
            <input type="text" name="username"><br>
            <label>Senha:</label><br>
            <input type="password" name="password"><br><br>
            <input type="submit" value="Entrar">
        </form>
    </body>
    </html>
    """)

@app.route('/hello', methods=['GET'])
def hello():
    """
    Rota de saudação
    ---
    responses:
      200:
        description: Retorna uma saudação
    """
    return jsonify(message="Olá, mundo!")

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
      - name: b
        in: query
        type: number
        required: true
    responses:
      200:
        description: O resultado da soma
    """
    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 0))
    return jsonify(resultado=a + b)


@app.route('/get_production_data', methods=['GET'])
def get_production_data():
    """
    Obtém dados de produção de uva da Embrapa.
    ---
    parameters:
      - name: ano
        in: query
        type: number
        required: true
    
    responses:
      200:
        description: Dados de produção de uva
        schema:
          type: object
          properties:
            categoria:
              type: object
              description: Dicionário com os dados da categoria e seus subitens
            total:
              type: number
              description: Total da categoria
      500:
        description: Internal Server Error. Erro inesperado 

      502:
        description: 502 Bad Gateway. Falhas na comunicação com serviços.
    """
    ano = float(request.args.get("ano", 0))

    # Aqui você chamaria a função que obtém os dados da Embrapa
    # Exemplo de chamada:
    dados = GetEmbrapaData().get_production_data(ano)
    
    
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)
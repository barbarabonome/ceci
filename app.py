from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/api/status')
def get_status():
    try:
        r = requests.get("https://www.diretodostrens.com.br/api/status", verify=False)
        if r.status_code == 200:
            dados = r.json()

            # Filtrando os códigos 4, 5, 8 e 9 com suas respectivas situações
            linhas_desejadas = [4, 5, 8, 9]
            linhas_filtradas = [
                {"codigo": linha['codigo'], "situacao": linha['situacao']}
                for linha in dados
                if linha['codigo'] in linhas_desejadas
            ]

            return jsonify({"linhas": linhas_filtradas})  # Envia apenas as linhas desejadas
        else:
            return jsonify({"erro": "Falha ao buscar dados", "status_code": r.status_code}), r.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

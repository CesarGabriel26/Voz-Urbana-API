from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import dotenv
import json
import os

from routes.usuario import usuarios_bp
from routes.reports import reports_bp
from routes.abaixo_assinados import petitions_bp
from routes.imagem import imagem_bp

app = Flask(__name__)
CORS(app)
dotenv.load_dotenv()

### Swagger configuration ###
SWAGGER_URL = '/docs'  # URL para acessar a documentação
API_URL = '/swagger.json'  # Caminho para o arquivo JSON de especificação Swagger

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI URL
    API_URL,  # Swagger arquivo JSON URL
    config={  # Configurações adicionais do Swagger UI
        'app_name': "API Voz Urbana"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(reports_bp, url_prefix='/reports')
app.register_blueprint(petitions_bp, url_prefix='/peticoes')
app.register_blueprint(imagem_bp, url_prefix='/imagem')

@app.route('/swagger.json')
def swagger_json():
    if os.path.exists("swagger_spec.json"):
        with open("swagger_spec.json", 'r') as json_file:
            swagger_spec = json.load(json_file)
            return swagger_spec
    else:
        return {}

@app.route('/')
def main():
    return "Olá Mundo!!!!"


if __name__ == "__main__":
    app.run()

from flask import Flask
from flask_cors import CORS

from routes.usuario import usuarios_bp
from routes.reports import reports_bp

app = Flask(__name__)
CORS(app)

#   

app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(reports_bp, url_prefix='/reports')
# app.register_blueprint(abaixo_assinado_bp, url_prefix='/abaixo_assinado')

@app.route('/')
def home():
    return "ROTA DE TESTE"
    
if __name__ == "__main__":
    app.run(port=5000, host="localhost", debug=True)
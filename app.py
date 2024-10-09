from flask import Flask
from flask_cors import CORS

from routes.usuario import usuarios_bp
from routes.reports import reports_bp
from routes.abaixo_assinados import petitions_bp

app = Flask(__name__)
CORS(app)

#   

app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(reports_bp, url_prefix='/reports')
app.register_blueprint(petitions_bp, url_prefix='/peticoes')

@app.route('/')
def home():
    return "ROTA DE TESTE"
    
if __name__ == "__main__":
    app.run()

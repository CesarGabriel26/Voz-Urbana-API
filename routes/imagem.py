from flask import Blueprint, request, jsonify
import requests
import os

imagem_bp = Blueprint('imagem', __name__)

def enviar_imagem_blob(imagem):
    url_blob = os.getenv("BLOB_URL")  # A URL do seu Blob Vercel
    headers = {
        "Authorization": f"Bearer {os.getenv('BLOB_READ_WRITE_TOKEN')}",  # Use sua chave de API do Blob
        "Content-Type": "application/octet-stream"  # Tipo de conteúdo do arquivo
    }
    
    response = requests.post(url_blob, headers=headers, data=imagem)

    if response.status_code == 200:
        return response.json().get("url")  # Retorna a URL da imagem enviada
    else:
        raise Exception(f"Erro ao enviar imagem para o Blob: {response.text}")

@imagem_bp.route('/upload', methods=['POST'])
def upload_imagem():
    arquivo = request.files.get('imagem')  # Supondo que a imagem está no campo 'imagem'
    
    if not arquivo:
        return jsonify({"message": "Nenhuma imagem fornecida"}), 400
    
    try:
        imagem = arquivo.read()
        
        # Enviar a imagem para o Blob e obter a URL
        url_imagem = enviar_imagem_blob(imagem)
        
        return jsonify({"message": "success", "content": url_imagem}), 200
        
    except Exception as e:
        return jsonify({"message": "Erro ao processar a imagem: " + str(e)}), 500

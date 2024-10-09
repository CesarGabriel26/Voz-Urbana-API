from flask import Blueprint, request, jsonify
import os
import vercel_blob


imagem_bp = Blueprint('imagem', __name__)

@imagem_bp.route('/upload', methods=['POST'])
def upload_imagem():
    arquivo = request.files.get('imagem')  # Supondo que a imagem está no campo 'imagem'
    
    if not arquivo:
        return jsonify({"error": "Nenhuma imagem fornecida"}), 400
    
    try:
        # Obtém o nome do arquivo
        nome_arquivo = arquivo.filename
        
        # Usa o método put da biblioteca vercel_blob para enviar a imagem
        data_imagem = vercel_blob.put(nome_arquivo, arquivo.read(), {})  # Envia o arquivo para o Blob

        return jsonify({"message": "success", "content": data_imagem}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro ao processar a imagem: " + str(e)}), 500

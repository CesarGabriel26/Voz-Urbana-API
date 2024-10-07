from flask import Blueprint, request, jsonify
from conexao import criar_conexao, fechar_conexao
from models import Petition

abaixo_assinado_bp = Blueprint('abaixo_assinado', __name__)

@abaixo_assinado_bp.route('/create', methods=['POST'])
def new_usuario():
    data = request.get_json()
    peticao = Petition.from_dict(data)
    
    conn = criar_conexao()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (id_usuario, titulo, conteudo, assinaturas) VALUES (%s, %s, %s, %s)",
            (peticao.id_usuario, peticao.titulo, peticao.conteudo, peticao.assinatura)
        )
        conn.commit()
        
        return jsonify({'message': 'User added successfully', 'content': peticao.to_dict()}), 201
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    
    finally:
        cursor.close()
        fechar_conexao(conn)

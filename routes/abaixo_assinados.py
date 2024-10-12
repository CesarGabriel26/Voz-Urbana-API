from flask import Blueprint, request, jsonify
from conexao import criar_conexao, fechar_conexao
from models import Petition
from psycopg2.extras import RealDictCursor

petitions_bp = Blueprint('peticoes', __name__)

@petitions_bp.route('/create', methods=['POST'])
def nova_peticao():
    data = request.get_json()
    petition = Petition.from_dict(data)
    
    conn = criar_conexao()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO peticoes (user_id, title, content, signatures, required_signatures) VALUES (%s, %s, %s, %s, %s)",
            (petition.user_id, petition.title, petition.content, petition.signatures, petition.required_signatures)
        )
        conn.commit()
        
        return jsonify({'message': 'Petition created successfully', 'content': petition.to_dict()}), 201
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@petitions_bp.route('/list', methods=['GET'])
def list_peticoes():
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("select * from peticoes")
        petitions = cursor.fetchall()
        
        if petitions:
            return jsonify({'message': 'Found', 'content': petitions}), 200
        else:
            return jsonify({'message': 'No petitions found', 'content': []}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@petitions_bp.route('/get_by_user/<int:user_id>', methods=['GET'])
def get_petitions_by_user(user_id):
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("SELECT * FROM peticoes WHERE user_id = %s", (user_id,))
        petitions = cursor.fetchall()
        
        if petitions:
            return jsonify({'content': petitions}), 200
        else:
            return jsonify({'message': 'No petitions found for this user'}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@petitions_bp.route('/update/<int:id>', methods=['PUT'])
def update_peticao(id):
    data = request.get_json()
    updated_petition = Petition.from_dict(data)
    
    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        # Verificar se a petição existe
        cursor.execute("SELECT * FROM peticoes WHERE id = %s", (id,))
        existing_petition = cursor.fetchone()

        if not existing_petition:
            return jsonify({'error': 'Petition not found'}), 404

        # Atualizar a petição
        cursor.execute("""
            UPDATE peticoes 
            SET user_id = %s, title = %s, content = %s, signatures = %s, required_signatures = %s
            WHERE id = %s
        """, (updated_petition.user_id, updated_petition.title, updated_petition.content, updated_petition.signatures, updated_petition.required_signatures, id))
        
        conn.commit()

        return jsonify({'message': 'Petition updated successfully', 'content': updated_petition.to_dict()}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@petitions_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_peticao(id):
    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        # Verificar se a petição existe
        cursor.execute("SELECT * FROM peticoes WHERE id = %s", (id,))
        petition = cursor.fetchone()

        if not petition:
            return jsonify({'error': 'Petition not found'}), 404

        # Deletar a petição
        cursor.execute("DELETE FROM peticoes WHERE id = %s", (id,))
        conn.commit()

        return jsonify({'message': 'Petition deleted successfully'}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@petitions_bp.route('/check_signatures/<int:id>', methods=['GET'])
def check_signatures(id):
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("SELECT signatures, required_signatures FROM peticoes WHERE id = %s", (id,))
        petition = cursor.fetchone()
        
        if petition:
            if petition['signatures'] >= petition['required_signatures']:
                return jsonify({'message': 'Petition has reached the required number of signatures'}), 200
            else:
                return jsonify({
                    'message': 'Petition has not yet reached the required number of signatures',
                    'content' : {
                        'current_signatures': petition['signatures'],
                        'required_signatures': petition['required_signatures']
                    }
                }), 200
        else:
            return jsonify({'error': 'Petition not found'}), 404
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

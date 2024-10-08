from flask import Blueprint, request, jsonify
from conexao import criar_conexao, fechar_conexao
import bcrypt

from models import User

usuarios_bp = Blueprint('usuarios', __name__)
SECRET_KEY = "ae26c5df0cbf451e2504f9ba5ab9d42f191939f65ce8e6a3f94787715db20811"

@usuarios_bp.route('/create', methods=['POST'])
def new_usuario():
    data = request.get_json()
    user = User.from_dict(data)
    
    conn = criar_conexao()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(user.senha.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, pfp, cpf) VALUES (%s, %s, %s, %s, %s)",
            (user.nome, user.email, hashed_password, user.pfp, user.cpf)
        )
        conn.commit()
        
        return jsonify({'message': 'User added successfully', 'content': user.to_dict()}), 201
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@usuarios_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(senha.encode('utf-8'), user['senha'].encode('utf-8')):
                return jsonify({'content': user}), 200
            else:
                return jsonify({'message': 'Invalid password'}), 401
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@usuarios_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        # Verificar se o usuário existe
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Deletar o usuário
        cursor.execute("DELETE FROM User WHERE id = %s", (id,))
        conn.commit()

        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@usuarios_bp.route('/update/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    updated_user = User.from_dict(data)
    
    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        # Verificar se o usuário existe
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        existing_user = cursor.fetchone()

        if not existing_user:
            return jsonify({'message': 'User not found'}), 404

        # Atualizar a senha, se for fornecida uma nova
        if updated_user.senha:
            hashed_password = bcrypt.hashpw(updated_user.senha.encode('utf-8'), bcrypt.gensalt())
        else:
            hashed_password = existing_user['senha']

        # Atualizar os dados do usuário
        cursor.execute("""
            UPDATE User 
            SET nome = %s, email = %s, senha = %s, foto = %s, cpf = %s 
            WHERE id = %s
        """, (updated_user.nome, updated_user.email, hashed_password, updated_user.pfp, updated_user.cpf, id))
        
        conn.commit()

        return jsonify({'message': 'User updated successfully', 'content': updated_user.to_dict()}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

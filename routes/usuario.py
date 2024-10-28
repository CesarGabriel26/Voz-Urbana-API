from flask import Blueprint, request, jsonify
from conexao import criar_conexao, fechar_conexao
from psycopg2.extras import RealDictCursor
import bcrypt

from models import User

usuarios_bp = Blueprint('usuarios', __name__)

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
            (user.nome, user.email, hashed_password.decode('utf-8'), user.pfp, user.cpf)
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
    cursor = conn.cursor(cursor_factory=RealDictCursor)  # Usando RealDictCursor para retornar resultados como dicionário
    
    try:
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user_data  = cursor.fetchone()

        if user_data :
            if bcrypt.checkpw(senha.encode('utf-8'), user_data['senha'].encode('utf-8')):
                user = User.from_dict(user_data)
                token = user.gerar_token()
                
                return jsonify({'message': 'Usuario Encontrado', 'content': token}), 200
            
            else:
                return jsonify({'error': 'Senha Incorreta'}), 401
        else:
            return jsonify({'error': 'Email ou Senha incorretos'}), 404
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@usuarios_bp.route('/passwordCheck/<int:id>', methods=['POST'])
def passwordCheck(id):
    data = request.get_json()
    senha = data.get('senha')

    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)  # Usando RealDictCursor para retornar resultados como dicionário
    
    try:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        user_data  = cursor.fetchone()

        if user_data :
            if bcrypt.checkpw(senha.encode('utf-8'), user_data['senha'].encode('utf-8')):
                return jsonify({'message': 'Senha Correta', 'content': True}), 200
            
            else:
                return jsonify({'error': 'Senha Incorreta'}), 401
        else:
            return jsonify({'error': 'Email ou Senha incorretos'}), 404
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@usuarios_bp.route('/get/<int:id>', methods=['GET'])
def get_usuario_by_id(id):
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # Verificar se o usuário existe
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'message': 'Found', "content": user}), 200
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
            return jsonify({'error': 'User not found'}), 404

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
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # Verificar se o usuário existe
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        existing_user = cursor.fetchone()

        if not existing_user:
            return jsonify({'error': 'User not found'}), 404

        # Atualizar a senha e/ou email e definir last_update se algum dos dois mudar
        update_last_update = False

        # Atualizar a senha, se fornecida e diferente da atual
        if updated_user.senha and not bcrypt.checkpw(updated_user.senha.encode('utf-8'), existing_user['senha'].encode('utf-8')):
            hashed_password = bcrypt.hashpw(updated_user.senha.encode('utf-8'), bcrypt.gensalt())
            update_last_update = True
        else:
            hashed_password = existing_user['senha']

        # Atualizar o email, se fornecido e diferente do existente
        if updated_user.email and updated_user.email != existing_user['email']:
            update_last_update = True

        # Executa a atualização
        query = ""
        if update_last_update :
            query = """ 
                UPDATE usuarios 
                SET nome = %s, email = %s, senha = %s, pfp = %s, cpf = %s, last_update = NOW() 
                WHERE id = %s 
            """ 
        else:
            query = """
            UPDATE usuarios 
                SET nome = %s, email = %s, senha = %s, pfp = %s, cpf = %s 
                WHERE id = %s
            """,
            
        cursor.execute(
            query
            (updated_user.nome, updated_user.email, hashed_password, updated_user.pfp, updated_user.cpf, id)
        )

        conn.commit()

        # Gera um novo token
        updated_user.senha = hashed_password  # Define a senha no objeto atualizado
        token = updated_user.gerar_token()  # Gera um novo token com os dados atualizados

        return jsonify({'message': 'User updated successfully', 'content': token}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@usuarios_bp.route('/verifyToken/<int:id>', methods=['GET'])
def verify_token(id):
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("SELECT last_update FROM usuarios WHERE id = %s", (id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'message': 'ok', 'content' : {'last_update': user['last_update']}}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

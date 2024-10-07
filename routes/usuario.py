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
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute(
            "INSERT INTO users (nome, email, senha, foto, cpf) VALUES (%s, %s, %s, %s, %s)",
            (user.nome, user.email, hashed_password, user.foto, user.cpf)
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
        user = cursor.fetchall()
        
        print(user)

        if user:
            print(senha.encode('utf-8'))
            print(user['password'].encode('utf-8'))

            if bcrypt.checkpw(senha.encode('utf-8'), user['password'].encode('utf-8')):
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

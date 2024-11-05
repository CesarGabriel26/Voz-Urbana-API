from flask import Blueprint, request, jsonify
from conexao import criar_conexao, fechar_conexao
from models import Petition
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta

petitions_bp = Blueprint('peticoes', __name__)

@petitions_bp.route('/create', methods=['POST'])
def nova_peticao():
    data = request.get_json()
    petition = Petition.from_dict(data)
    
    conn = criar_conexao()
    cursor = conn.cursor()

    data_limite = petition.data_limite if petition.data_limite else (datetime.now() + timedelta(days=30))  # Exemplo: 30 dias no futuro
    
    try:
        cursor.execute(
            """
            INSERT INTO petitions (user_id, titulo, content, required_signatures, data_limite, local)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                petition.user_id,
                petition.titulo,
                petition.content,
                petition.required_signatures,
                data_limite,
                petition.local
            )
        )
        conn.commit()
        return jsonify({'message': 'Petition created successfully'}), 201

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
        cursor.execute("SELECT * FROM petitions")
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

@petitions_bp.route('/get/<int:id>', methods=['GET'])
def get_petitions_by_id(id):
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("SELECT * FROM petitions WHERE id = %s", (id,))
        petition = cursor.fetchone()
        
        if petition:
            return jsonify({'content': petition}), 200
        else:
            return jsonify({'message': 'Petition not found'}), 404
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
        cursor.execute("SELECT * FROM petitions WHERE user_id = %s", (user_id,))
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
        cursor.execute("SELECT * FROM petitions WHERE id = %s", (id,))
        existing_petition = cursor.fetchone()

        if not existing_petition:
            return jsonify({'error': 'Petition not found'}), 404

        # Atualizar a petição
        cursor.execute(""" 
            UPDATE petitions 
            SET user_id = %s, titulo = %s, content = %s, signatures = %s, required_signatures = %s, 
                aberto = %s, data_limite = %s, local = %s, categoria = %s 
            WHERE id = %s
        """, (
            updated_petition.user_id,
            updated_petition.title,
            updated_petition.content,
            updated_petition.signatures,
            updated_petition.required_signatures,
            updated_petition.aberto,
            updated_petition.data_limite,
            updated_petition.local,
            updated_petition.categoria,
            id
        ))
        
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
        cursor.execute("SELECT * FROM petitions WHERE id = %s", (id,))
        petition = cursor.fetchone()

        if not petition:
            return jsonify({'error': 'Petition not found'}), 404

        # Deletar a petição
        cursor.execute("DELETE FROM petitions WHERE id = %s", (id,))
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
        cursor.execute("SELECT signatures, required_signatures FROM petitions WHERE id = %s", (id,))
        petition = cursor.fetchone()
        
        if petition:
            if petition['signatures'] >= petition['required_signatures']:
                return jsonify({'message': 'Petition has reached the required number of signatures'}), 200
            else:
                return jsonify({
                    'message': 'Petition has not yet reached the required number of signatures',
                    'content': {
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

@petitions_bp.route('/check_all_open_petitions', methods=['GET'])
def check_all_open_petitions():
    conn = criar_conexao()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM petitions WHERE aberto = TRUE")
            result = cursor.fetchall()

            if not result:
                return jsonify({'message': 'No open petitions found'}), 200
            
            open_petitions = []
            data_atual = datetime.now()

            for row in result:
                petition_id, data_limite = row[0], row[7]  # Certifique-se de que o índice corresponde ao data_limite
                
                if data_limite:
                    time_remaining = data_limite - data_atual
                    
                    if time_remaining.total_seconds() > 0:
                        dias_restantes = time_remaining.days
                        horas_restantes = time_remaining.seconds // 3600
                        minutos_restantes = (time_remaining.seconds % 3600) // 60

                        open_petitions.append(
                            {
                                'open_petitions': Petition.to_dict(row),
                                "tempo_restante": {
                                    'dias_restantes': dias_restantes,
                                    'horas_restantes': horas_restantes,
                                    'minutos_restantes': minutos_restantes
                                }
                            }
                        )
                    else:
                        try:
                            cursor.execute("UPDATE petitions SET aberto = FALSE WHERE id = %s", (petition_id,))
                            conn.commit()
                        except Exception as update_err:
                            return jsonify({'error': f'Failed to update petition {petition_id}: {str(update_err)}'}), 500

            return jsonify({'message': 'Open petitions', 'content': open_petitions}), 200
            
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        fechar_conexao(conn)

@petitions_bp.route('/check_timer/<int:petition_id>', methods=['GET'])
def check_timer(petition_id):
    conn = criar_conexao()
    
    try:
        with conn.cursor() as cursor:
            # Busca a petição pelo ID, apenas se estiver aberta
            cursor.execute("SELECT data_limite FROM petitions WHERE id = %s ", (petition_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({'error': 'Petition not found or not open'}), 404
            
            data_limite = result[0]
            data_atual = datetime.now()

            if data_limite and data_limite <= data_atual:
                try:
                    # Fecha a petição se o tempo se esgotou
                    cursor.execute("UPDATE petitions SET aberto = FALSE WHERE id = %s", (petition_id,))
                    conn.commit()
                    return jsonify({'message': 'Petition has been closed due to time expiration'}), 200
                except Exception as update_err:
                    return jsonify({'error': str(update_err)}), 500
            
            time_remaining = data_limite - data_atual
            
            dias_restantes = time_remaining.days
            horas_restantes = time_remaining.seconds // 3600
            minutos_restantes = (time_remaining.seconds % 3600) // 60

            return jsonify({
                'message': 'Time remaining for the petition',
                'tempo_restante': {
                    'dias_restantes': dias_restantes,
                    'horas_restantes': horas_restantes,
                    'minutos_restantes': minutos_restantes
                }
            }), 200
            
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        fechar_conexao(conn)

from flask import Blueprint, request, jsonify
from conexao import criar_conexao, fechar_conexao
from psycopg2.extras import RealDictCursor
from models import Report

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.cluster import KMeans

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/create', methods=['POST'])
def novo_report():
    data = request.get_json()

    # Verifique se user_id está presente
    if 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400

    report = Report.from_dict(data)
    
    conn = criar_conexao()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO reports (user_id, latitude, longitude, titulo, conteudo, imagem, data, adress) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (report.user_id, report.latitude, report.longitude, report.titulo, report.conteudo, report.imagem, report.data, report.adress)
        )
        conn.commit()
        
        return jsonify({'message': 'Report added successfully', 'content': report.to_dict()}), 201
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@reports_bp.route('/list', methods=['GET'])
def list_reports():
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("SELECT * FROM reports")
        reports = cursor.fetchall()
        
        if reports:
            return jsonify({'content': reports}), 200
        else:
            return jsonify({'message': 'empty', 'content': []}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@reports_bp.route('/get/<int:id>', methods=['GET'])
def get_petitions_by_id(id):
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("SELECT * FROM reports WHERE id = %s", (id,))
        petitions = cursor.fetchone()
        
        if petitions:
            return jsonify({'message': "found", 'content': petitions}), 200
        else:
            return jsonify({'message': 'report not found'}), 404
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@reports_bp.route('/get_by_user/<int:user_id>', methods=['GET'])
def get_reports_by_user(user_id):
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("SELECT * FROM reports WHERE user_id = %s", (user_id,))
        reports = cursor.fetchall()
        
        if reports:
            return jsonify({'content': reports}), 200
        else:
            return jsonify({'error': 'No reports found for this user'}), 404
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@reports_bp.route('/update/<int:id>', methods=['PUT'])
def update_report(id):
    data = request.get_json()
    updated_report = Report.from_dict(data)
    
    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        # Verificar se o report existe
        cursor.execute("SELECT * FROM reports WHERE id = %s", (id,))
        existing_report = cursor.fetchone()

        if not existing_report:
            return jsonify({'error': 'Report not found'}), 404

        # Atualizar o report
        cursor.execute(
            """
                UPDATE reports
                SET titulo = %s, conteudo = %s, data = %s, aceito = %s
                WHERE id = %s
            """, 
            (updated_report.titulo, updated_report.conteudo, updated_report.data, updated_report.aceito, id)
        )
        
        conn.commit()

        return jsonify({'message': 'Report updated successfully', 'content': updated_report.to_dict()}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)

@reports_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_report(id):
    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        # Verificar se o report existe
        cursor.execute("SELECT * FROM reports WHERE id = %s", (id,))
        report = cursor.fetchone()

        if not report:
            return jsonify({'error': 'Report not found'}), 404

        # Deletar o report
        cursor.execute("DELETE FROM reports WHERE id = %s", (id,))
        conn.commit()

        return jsonify({'message': 'Report deleted successfully'}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)
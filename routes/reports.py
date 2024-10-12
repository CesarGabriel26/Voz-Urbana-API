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
            "INSERT INTO reports (user_id, latitude, longitude, titulo, conteudo, imagem, data) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (report.user_id, report.latitude, report.longitude, report.titulo, report.conteudo, report.imagem, report.data)
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
                UPDATE Report 
                SET titulo = %s, conteudo = %s, data = %s, aceito= %s
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
        cursor.execute("DELETE FROM Report WHERE id = %s", (id,))
        conn.commit()

        return jsonify({'message': 'Report deleted successfully'}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        fechar_conexao(conn)


# @reports_bp.route('/list/grouped', methods=['GET'])
# def list_grouped_reports():
#     conn = criar_conexao()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
    
#     try:
#         cursor.execute("SELECT * FROM reports")
#         reports = cursor.fetchall()
        
#         if not reports:
#             return jsonify({'message': 'No reports found', 'content': []}), 200
        
#         # Extraindo títulos e conteúdos para o agrupamento
#         documents = [f"{report['titulo']} {report['conteudo']}" for report in reports]

#         # Vetorização
#         stop_words_portuguese = ['e', 'a', 'o', 'que', 'de', 'do', 'da', 'em', 'um', 'para', 'com', 'no', 'pro', 'pra']  # Adicione mais conforme necessário
#         vectorizer = TfidfVectorizer(stop_words=stop_words_portuguese)
#         X = vectorizer.fit_transform(documents)

#         # Agrupamento
#         num_clusters = min(3, len(reports))  # Ajusta o número de clusters para o número de relatórios
#         kmeans = KMeans(n_clusters=num_clusters, random_state=0)
#         kmeans.fit(X)

#         # Adicionando o cluster a cada reclamação
#         for i, report in enumerate(reports):
#             report['cluster'] = int(kmeans.labels_[i])  # Armazenando como inteiro

#         # Extraindo os principais tópicos
#         def get_top_keywords(cluster, n_terms=5):
#             order_centroids = cluster.cluster_centers_.argsort()[:, ::-1]
#             terms = vectorizer.get_feature_names_out()
#             top_terms = []
#             for i in range(cluster.n_clusters):
#                 top_terms.append([terms[ind] for ind in order_centroids[i, :n_terms]])
#             return top_terms

#         top_keywords = get_top_keywords(kmeans)

#         # Estruturando a resposta
#         grouped_reports = {
#             "groups": [],
#             "topics": {}
#         }

#         for i in range(num_clusters):
#             group = [report for report in reports if report['cluster'] == i]
#             grouped_reports['groups'].append({
#                 "cluster_id": i,
#                 "reports": group,
#                 "topics": top_keywords[i]
#             })

#         return jsonify(grouped_reports), 200
        
#     except Exception as err:
#         return jsonify({'error': str(err)}), 500
#     finally:
#         cursor.close()
#         fechar_conexao(conn)

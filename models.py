import jwt
import os

class User:
    def __init__(self, nome, senha, email, cpf, created_at=None, updated_at=None, type=0, pfp=None, user_id=None):
        self.id = user_id
        self.nome = nome
        self.senha = senha
        self.email = email
        self.cpf = cpf
        self.pfp = pfp
        self.type = type
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'pfp': self.pfp,
            'cpf': self.cpf,
            'type': self.type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data['nome'],
            email=data['email'],
            senha=data.get('senha'),
            pfp=data.get('pfp'),
            cpf=data['cpf'],
            user_id=data.get('id'),
            type=data.get('type', 0),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def gerar_token(self):
        payload = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'pfp': self.pfp,
            'cpf': self.cpf,
            'type': self.type,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ') if self.updated_at else None
        }
        token = jwt.encode(payload, os.getenv("JWT_KEY"), algorithm='HS256')
        return token

class Report:
    def __init__(self, latitude, longitude, titulo, conteudo, imagem, data, user_id, adress="", status=0, prioridade=2, categoria=None, report_id=None, aceito=False):
        self.id = report_id
        self.latitude = latitude
        self.longitude = longitude
        self.titulo = titulo
        self.conteudo = conteudo
        self.imagem = imagem
        self.aceito = aceito
        self.data = data
        self.user_id = user_id
        self.adress = adress
        self.status = status
        self.prioridade = prioridade
        self.categoria = categoria

    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'titulo': self.titulo,
            'conteudo': self.conteudo,
            'imagem': self.imagem,
            'aceito': self.aceito,
            'data': self.data,
            'user_id': self.user_id,
            'adress': self.adress,
            'status': self.status,
            'prioridade': self.prioridade,
            'categoria': self.categoria
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            latitude=data['latitude'],
            longitude=data['longitude'],
            titulo=data['titulo'],
            conteudo=data['conteudo'],
            imagem=data['imagem'],
            aceito=data.get('aceito', False),
            data=data['data'],
            report_id=data.get('id'),
            adress=data.get('adress', ""),
            user_id=data['user_id'],
            status=data.get('status', 0),
            prioridade=data.get('prioridade', 2),
            categoria=data.get('categoria')
        )

class Petition:
    def __init__(
    self, user_id, title, content, signatures=0, required_signatures=100, 
    aberto=False, data=None, data_limite=None, data_conclusao=None, 
    status=0, causa=None, motivo_encerramento=None, local=None, 
    categoria=None, total_apoios=0, data_ultima_atualizacao=None, 
    petition_id=None
):
        self.id = petition_id
        self.user_id = user_id
        self.causa = causa
        self.content = content
        self.signatures = signatures
        self.required_signatures = required_signatures
        self.aberto = aberto
        self.data = data
        self.data_limite = data_limite
        self.data_conclusao = data_conclusao
        self.status = status
        self.causa = causa
        self.motivo_encerramento = motivo_encerramento
        self.local = local
        self.categoria = categoria
        self.total_apoios = total_apoios
        self.data_ultima_atualizacao = data_ultima_atualizacao

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'causa': self.causa,
            'content': self.content,
            'signatures': self.signatures,
            'required_signatures': self.required_signatures,
            'aberto': self.aberto,
            'data': self.data,
            'data_limite': self.data_limite,
            'data_conclusao': self.data_conclusao,
            'status': self.status,
            'causa': self.causa,
            'motivo_encerramento': self.motivo_encerramento,
            'local': self.local,
            'categoria': self.categoria,
            'total_apoios': self.total_apoios,
            'data_ultima_atualizacao': self.data_ultima_atualizacao
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data['user_id'],
            title=data['title'],
            content=data['content'],
            signatures=data.get('signatures', 0),
            required_signatures=data.get('required_signatures', 100),
            aberto=data.get('aberto', False),
            data=data.get('data'),
            data_limite=data.get('data_limite'),
            data_conclusao=data.get('data_conclusao'),
            status=data.get('status', 0),
            motivo_encerramento=data.get('motivo_encerramento'),
            local=data.get('local'),
            categoria=data.get('categoria'),
            total_apoios=data.get('total_apoios', 0),
            data_ultima_atualizacao=data.get('data_ultima_atualizacao'),
            petition_id=data.get('id')
        )

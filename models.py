import jwt
import os

class User:
    def __init__(self, nome, senha, email, cpf, last_update, pfp=None, user_id=None):
        self.id = user_id
        self.nome = nome
        self.senha = senha
        self.email = email
        self.cpf = cpf
        self.pfp = pfp
        self.last_update = last_update

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'pfp': self.pfp,
            'cpf': self.cpf,
            'last_update' : self.last_update
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
            last_update=data['last_update']
        )

    def gerar_token(self):
        payload = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'pfp': self.pfp,
            'cpf': self.cpf,
            'last_update': self.last_update.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
        token = jwt.encode(payload, os.getenv("JWT_KEY"), algorithm='HS256')
        return token

class Report:
    def __init__(self, latitude, longitude, titulo, conteudo, imagem, data, user_id, adress, report_id=None, aceito=False):
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
            'adress' : self.adress,
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
            user_id=data['user_id']
        )

class Petition:
    def __init__(self, user_id, title, content, signatures=0, required_signatures=100, status=0, data_limite=None, petition_id=None):
        self.id = petition_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.signatures = signatures
        self.required_signatures = required_signatures
        self.status = status
        self.data_limite = data_limite

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'signatures': self.signatures,
            'required_signatures': self.required_signatures,
            'status': self.status,
            'data_limite': self.data_limite
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data['user_id'],
            title=data['title'],
            content=data['content'],
            signatures=data.get('signatures', 0),
            required_signatures=data.get('required_signatures', 100),
            status=data.get('status', 0),
            data_limite=data.get('data_limite'),
            petition_id=data.get('id')
        )

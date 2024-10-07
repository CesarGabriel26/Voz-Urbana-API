class User:
    def __init__(self, nome, senha, email, cpf, pfp=None, user_id=None):
        self.id = user_id
        self.nome = nome
        self.senha = senha
        self.email = email
        self.cpf = cpf
        self.pfp = pfp

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'foto': self.foto,
            'cpf': self.cpf,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data['username'],
            email=data['email'],
            senha=data['senha'],
            foto=data.get('foto'),
            cpf=data['cpf'],
            user_id=data.get('id')
        )

class Report:
    def __init__(self, latitude, longitude, titulo, conteudo, data, report_id=None):
        self.id = report_id
        self.latitude = latitude
        self.longitude = longitude
        self.titulo = titulo
        self.conteudo = conteudo
        self.data = data

    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'titulo': self.titulo,
            'conteudo': self.conteudo,
            'data': self.data
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            latitude=data['latitude'],
            longitude=data['longitude'],
            titulo=data['titulo'],
            conteudo=data['conteudo'],
            data=data['data'],
            report_id=data.get('id')
        )

class Petition:
    def __init__(self, user_id, title, content, signatures=0, petition_id=None):
        self.id = petition_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.signatures = signatures

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'signatures': self.signatures
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data['user_id'],
            title=data['title'],
            content=data['content'],
            signatures=data.get('signatures', 0),
            id=data.get('id')
        )

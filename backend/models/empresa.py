from database import db

class Empresa(db.Model):
    __tablename__ = 'empresa'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    contato_telefone = db.Column(db.String(20), nullable=False)
    
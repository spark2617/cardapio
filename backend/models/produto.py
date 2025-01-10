from database import db

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    link_imagem = db.Column(db.String(200), nullable=True)
    preco_produto = db.relationship('PrecoProduto', backref='produto', lazy=True)
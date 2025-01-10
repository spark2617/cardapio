from database import db

class PrecoProduto(db.Model):
    __tablename__ = 'preco_produto'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=True)
    preco = db.Column(db.Float, nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)

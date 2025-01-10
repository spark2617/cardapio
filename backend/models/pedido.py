from database import db

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    nome_do_cliente = db.Column(db.String(100), nullable=False)
    lista_preco_produto = db.relationship('PrecoProduto', secondary='pedido_preco_produto', lazy='subquery',
                                          backref=db.backref('pedidos', lazy=True))
    endereco = db.Column(db.String(200), nullable=False)
    contato_cliente = db.Column(db.String(20), nullable=False)
    pendente = db.Column(db.Boolean, default=True)

# Tabela de Associação para Pedido e PrecoProduto
pedido_preco_produto = db.Table(
    'pedido_preco_produto',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id'), primary_key=True),
    db.Column('preco_produto_id', db.Integer, db.ForeignKey('preco_produto.id'), primary_key=True)
)
from flask import Flask
from routes.empresa import empresa_routes
from routes.pedido import pedido_routes
from routes.preco_produto import preco_produto_routes
from routes.produto import produto_routes
from database import db
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')
db.init_app(app)


with app.app_context():
    db.create_all()

# Rotas
app.register_blueprint(empresa_routes)
app.register_blueprint(produto_routes)
app.register_blueprint(preco_produto_routes)
app.register_blueprint(pedido_routes)


if __name__ == '__main__':
    app.run(debug=True)


from flask import Blueprint, request, jsonify
from models.produto import Produto
from database import db
from utils import verificar_admin
from routes.validacao import validar_campos


produto_routes = Blueprint('produto_routes', __name__)


# Criar Produto (POST)
@produto_routes.route('/produtos', methods=['POST'])
def criar_produto():
    verificacao = verificar_admin()
    if verificacao: 
        return verificacao

    dados = request.json

    # Validação dos campos
    campos_obrigatorios = {
        'nome': str,
        'categoria': str,
        'link_imagem': str
    }
    erros = validar_campos(dados, campos_obrigatorios)

    if erros:
        return jsonify({'errors': erros}), 400

    novo_produto = Produto(
        nome=dados['nome'],
        categoria=dados['categoria'],
        link_imagem=dados.get('link_imagem'),
    )
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({'message': 'Produto criado com sucesso!'}), 201

# Listar Produtos (GET)
@produto_routes.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([
        {
            'id': p.id,
            'nome': p.nome,
            'categoria': p.categoria,
            'link_imagem': p.link_imagem,
        } for p in produtos
    ])

# Atualizar Produto (PUT)
@produto_routes.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    verificacao = verificar_admin()
    if verificacao: 
        return verificacao

    produto = Produto.query.get_or_404(id)
    dados = request.json

    # Validação dos campos
    campos_obrigatorios = {
        'nome': str,
        'categoria': str,
        'link_imagem': str
    }
    erros = validar_campos(dados, campos_obrigatorios)

    if erros:
        return jsonify({'errors': erros}), 400

    produto.nome = dados['nome']
    produto.categoria = dados['categoria']
    produto.link_imagem = dados.get('link_imagem', produto.link_imagem)

    db.session.commit()
    return jsonify({'message': 'Produto atualizado com sucesso!'})

# Deletar Produto (DELETE)
@produto_routes.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    verificacao = verificar_admin()
    if verificacao: 
        return verificacao

    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'message': 'Produto deletado com sucesso!'})

from flask import Blueprint, request, jsonify
from models.preco_produto import PrecoProduto
from models.produto import Produto
from models.empresa import Empresa
from database import db
from utils import verificar_admin
from routes.validacao import validar_campos

preco_produto_routes = Blueprint('preco_produto_routes', __name__)

# Criar PrecoProduto (POST)
@preco_produto_routes.route('/precos', methods=['POST'])
def criar_preco_produto():
    verificacao = verificar_admin()
    if verificacao:
        return verificacao

    dados = request.json

    # Validação dos campos obrigatórios
    campos_obrigatorios = {
        'descricao': str,
        'preco': (int, float),
        'produto_id': int,
        'empresa_id': int
    }
    erros = validar_campos(dados, campos_obrigatorios)

    if erros:
        return jsonify({'errors': erros}), 400

    # Verificar se a empresa existe
    empresa = Empresa.query.get(dados['empresa_id'])
    if not empresa:
        return jsonify({'error': f"Empresa com ID {dados['empresa_id']} não encontrada."}), 404

    # Verificar se o produto existe
    produto = Produto.query.get(dados['produto_id'])
    if not produto:
        return jsonify({'error': f"Produto com ID {dados['produto_id']} não encontrado."}), 404

    # Criar o novo preço do produto
    novo_preco = PrecoProduto(
        descricao=dados['descricao'],
        preco=dados['preco'],
        produto_id=dados['produto_id'],
        empresa_id=dados['empresa_id']
    )
    db.session.add(novo_preco)
    db.session.commit()
    return jsonify({'message': 'Preço do produto criado com sucesso!'}), 201


# Listar PrecoProduto por Empresa (GET)
@preco_produto_routes.route('/precos/empresa/id/<int:empresa_id>', methods=['GET'])
def listar_precos(empresa_id):
    # Verificar se a empresa existe
    empresa = Empresa.query.get(empresa_id)
    if not empresa:
        return jsonify({'error': f"Empresa com ID {empresa_id} não encontrada."}), 404

    # Filtra os preços pela empresa_id
    precos = PrecoProduto.query.filter_by(empresa_id=empresa_id).all()

    return jsonify([{
        'id': p.id,
        'descricao': p.descricao,
        'preco': p.preco,
        'produto': {
            'id': p.produto.id,
            'nome': p.produto.nome,
            'categoria': p.produto.categoria,
            'link_imagem': p.produto.link_imagem,
        },
        'empresa_id': p.empresa_id
    } for p in precos])


@preco_produto_routes.route('/precos/empresa/<string:nome_empresa>', methods=['GET'])
def listar_precos_por_nome_empresa(nome_empresa):
    # Verificar se a empresa com o nome fornecido existe
    empresa = Empresa.query.filter(Empresa.nome.ilike(f"%{nome_empresa}%")).first()
    if not empresa:
        return jsonify({'error': f"Empresa com nome '{nome_empresa}' não encontrada."}), 404

    # Filtrar os preços pela empresa encontrada
    precos = PrecoProduto.query.filter_by(empresa_id=empresa.id).all()

    return jsonify([{
        'id': p.id,
        'descricao': p.descricao,
        'preco': p.preco,
        'produto': {
            'id': p.produto.id,
            'nome': p.produto.nome,
            'categoria': p.produto.categoria,
            'link_imagem': p.produto.link_imagem,
        },
        'empresa_id': p.empresa_id
    } for p in precos])



# Deletar PrecoProduto (DELETE)
@preco_produto_routes.route('/precos/<int:id>', methods=['DELETE'])
def deletar_precos(id):
    verificacao = verificar_admin()
    if verificacao:
        return verificacao

    preco = PrecoProduto.query.get_or_404(id)
    db.session.delete(preco)
    db.session.commit()
    return jsonify({'message': 'Preço deletado com sucesso!'})


# Listar Categorias (GET)
@preco_produto_routes.route('/categorias', methods=['GET'])
def listar_categoria():
    empresa_id = request.args.get('empresa_id', type=str)

    if empresa_id:
        # Verificar se a empresa existe
        empresa = Empresa.query.get(empresa_id)
        if not empresa:
            return jsonify({'error': f"Empresa com ID {empresa_id} não encontrada."}), 404

        precos = PrecoProduto.query.filter_by(empresa_id=empresa_id).all()
    else:
        precos = PrecoProduto.query.all()

    # Criar uma lista de categorias únicas
    categorias = list({p.produto.categoria for p in precos})

    return jsonify({'categorias': categorias})

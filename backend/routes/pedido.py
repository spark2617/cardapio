from flask import Blueprint, request, jsonify
from models.pedido import Pedido
from models.preco_produto import PrecoProduto
from database import db
from utils import verificar_admin
from routes.validacao import validar_campos  # Assumindo um módulo para validação
from services.enviar_whatsapp_vendedor import enviar_whatsapp_vendedor


pedido_routes = Blueprint('pedido_routes', __name__)

# Criar Pedido (POST)
@pedido_routes.route('/pedidos', methods=['POST'])
def criar_pedido():
    try:
        # Recebe os dados do pedido
        dados = request.json

        

        # Validação dos campos obrigatórios
        campos_obrigatorios = {
            'nome_do_cliente': str,
            'endereco': str,
            'contato_cliente': str
        }
        erros = validar_campos(dados, campos_obrigatorios)

        if erros:
            return jsonify({'errors': erros}), 400

        # Cria o pedido
        novo_pedido = Pedido(
            nome_do_cliente=dados['nome_do_cliente'],
            endereco=dados['endereco'],
            contato_cliente=dados['contato_cliente'],
            pendente=dados.get('pendente', True)
        )
        db.session.add(novo_pedido)

        # Associa produtos ao pedido
        for preco_produto_id in dados.get('lista_preco_produto', []):
            preco_produto = PrecoProduto.query.get(preco_produto_id)
            if preco_produto:
                novo_pedido.lista_preco_produto.append(preco_produto)
            else:
                return jsonify({'error': f'Produto com ID {preco_produto_id} não encontrado.'}), 404

        # Salva no banco de dados
        db.session.commit()

        enviar_whatsapp_vendedor(pedido=novo_pedido)

        return jsonify({'message': 'Pedido criado com sucesso!'}), 201

    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor.'}), 500

# Listar Pedidos (GET)
@pedido_routes.route('/pedidos', methods=['GET'])
def listar_pedidos():
    empresa_id = request.args.get('empresa_id', type=int)

    if empresa_id:
        pedidos = Pedido.query.join(PrecoProduto, Pedido.lista_preco_produto).filter(
            PrecoProduto.empresa_id == empresa_id).all()
    else:
        pedidos = Pedido.query.all()

    return jsonify([
        {
            'id': p.id,
            'nome_do_cliente': p.nome_do_cliente,
            'endereco': p.endereco,
            'contato_cliente': p.contato_cliente,
            'pendente': p.pendente,
            'lista_preco_produto': [
                {
                    'id': pp.id,
                    'descricao': pp.descricao,
                    'preco': pp.preco
                } for pp in p.lista_preco_produto
            ]
        } for p in pedidos
    ])

# Atualizar Pedido (PUT)
@pedido_routes.route('/pedidos/<int:id>', methods=['PUT'])
def atualizar_pedido(id):
    try:
        pedido = Pedido.query.get_or_404(id)
        dados = request.json

        # Validação dos campos obrigatórios
        campos_obrigatorios = {
            'nome_do_cliente': str,
            'endereco': str,
            'contato_cliente': str,
            'pendente': bool
        }
        erros = validar_campos(dados, campos_obrigatorios)

        if erros:
            return jsonify({'errors': erros}), 400

        # Atualiza os dados do pedido
        pedido.nome_do_cliente = dados['nome_do_cliente']
        pedido.endereco = dados['endereco']
        pedido.contato_cliente = dados['contato_cliente']
        pedido.pendente = dados['pendente']
        db.session.commit()

        return jsonify({'message': 'Pedido atualizado com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor.'}), 500

# Deletar Pedido (DELETE)
@pedido_routes.route('/pedidos/<int:id>', methods=['DELETE'])
def deletar_pedido(id):
    verificacao = verificar_admin()
    if verificacao: 
        return verificacao

    pedido = Pedido.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({'message': 'Pedido deletado com sucesso!'}), 200

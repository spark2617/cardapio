from flask import Blueprint, request, jsonify
from models.empresa import Empresa
from database import db
from utils import verificar_admin
from routes.validacao import validar_campos

empresa_routes = Blueprint('empresa_routes', __name__)

# Criar Empresa (POST)
@empresa_routes.route('/empresas', methods=['POST'])
def criar_empresa():
    verificacao = verificar_admin()
    if verificacao: 
        return verificacao

    dados = request.json

    # Validação dos campos
    campos_obrigatorios = {
        'nome': str,
        'contato_telefone': str,
    }
    erros = validar_campos(dados, campos_obrigatorios)

    if erros:
        return jsonify({'errors': erros}), 400

    nova_empresa = Empresa(
        nome=dados['nome'],
        contato_telefone=dados['contato_telefone']
    )
    db.session.add(nova_empresa)
    db.session.commit()
    return jsonify({'message': 'Empresa criada com sucesso!'}), 201

# Listar Empresas (GET)
@empresa_routes.route('/empresas', methods=['GET'])
def listar_empresas():
    empresas = Empresa.query.all()
    return jsonify([
        {
            'id': e.id,
            'nome': e.nome,
            'contato_telefone': e.contato_telefone
        } for e in empresas
    ])

# Buscar Empresa por ID (GET)
@empresa_routes.route('/empresas/<int:id>', methods=['GET'])
def buscar_id_empresas(id):
    empresas = Empresa.query.get_or_404(id)
    return jsonify({
        'id': empresas.id,
        'nome': empresas.nome,
        'contato_telefone': empresas.contato_telefone
    })

# Atualizar Empresa (PUT)
@empresa_routes.route('/empresas/<int:id>', methods=['PUT'])
def atualizar_empresa(id):
    verificacao = verificar_admin()
    if verificacao: 
        return verificacao

    empresa = Empresa.query.get_or_404(id)
    dados = request.json

    # Validação dos campos
    campos_obrigatorios = {
        'nome': str,
        'contato_telefone': str,
    }
    erros = validar_campos(dados, campos_obrigatorios)

    if erros:
        return jsonify({'errors': erros}), 400

    empresa.nome = dados['nome']
    empresa.contato_telefone = dados['contato_telefone']
    db.session.commit()
    return jsonify({'message': 'Empresa atualizada com sucesso!'})

# Deletar Empresa (DELETE)
@empresa_routes.route('/empresas/<int:id>', methods=['DELETE'])
def deletar_empresa(id):
    verificacao = verificar_admin()
    if verificacao: 
        return verificacao

    empresa = Empresa.query.get_or_404(id)
    db.session.delete(empresa)
    db.session.commit()
    return jsonify({'message': 'Empresa deletada com sucesso!'})

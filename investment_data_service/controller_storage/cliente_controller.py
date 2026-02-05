import sqlite3
from flask import Blueprint, request, jsonify
from ..repository.database import (     
     insert_user,insert_transacao,
     buscar_user_por_cpf, buscar_user_por_telefone,buscar_user_por_email,
     atualizar_user, delete_user,
     atualizar_senha_por_id
)


cliente_bp = Blueprint("clientes", __name__)


@cliente_bp.route("/clientes", methods = ["POST"])
def criar_clientes():
    dados = request.get_json()
    telefone = dados.get("telefone")
    
    if isinstance(telefone, list):
        telefone = telefone[0]

    dados["telefone"] = telefone

    try:
        user_id = insert_user(
            dados.get("nome"),
            dados.get("cpf"),
            dados.get("email"),
            dados.get("telefone"),
            dados.get("correntista"),
            dados.get("score_credito"),
            dados.get("saldo_cc"),
            dados.get("admin"),
            dados.get("senha")
        )
    except sqlite3.IntegrityError:
        return jsonify({"erro": "CPF, email ou telefone já cadastrados"}), 400

    dados["id"] = user_id
    return jsonify(dados), 201

@cliente_bp.route("/clientes/transacao", methods=["POST"])
def criar_transacao():
    dados = request.get_json()

    if not dados.get("cliente_id") or not dados.get("tipo") or not dados.get("valor"):
        return jsonify({"erro": "Campos obrigatórios: cliente_id, tipo, valor"}), 400

    try:
        transacao_id = insert_transacao(
            dados.get("cliente_id"),
            dados.get("tipo"),
            dados.get("valor"),
            dados.get("descricao")
        )
    except sqlite3.IntegrityError:
        return jsonify({"erro": "Cliente não existe ou dados da transação inválidos"}), 400

    dados["id_transacao"] = transacao_id
    return jsonify(dados), 201


@cliente_bp.route("/clientes/buscar/cpf/<cpf>", methods=["GET"])
def buscar_cpf_user(cpf):
    linha = buscar_user_por_cpf(cpf)

    if not linha:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    clientes = {
        "id": linha[0],
        "nome": linha[1],
        "cpf": linha[2],
        "email": linha[3],
        "telefone": linha[4],
        "correntista": linha[5],
        "score_credito": linha[6],
        "saldo_cc": linha[7],
        "admin": linha[8]
    }
    return jsonify(clientes), 200

@cliente_bp.route("/clientes/buscar/telefone/<telefone>", methods=["GET"])
def buscar_telefone_user(telefone):
    linha = buscar_user_por_telefone(telefone)

    if not linha:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    clientes = {
        "id": linha[0],
        "nome": linha[1],
        "cpf": linha[2],
        "email": linha[3],
        "telefone": linha[4],
        "correntista": linha[5],
        "score_credito": linha[6],
        "saldo_cc": linha[7],
        "admin": linha[8]
    }
    return jsonify(clientes), 200

@cliente_bp.route("/clientes/buscar/email/<email>", methods=["GET"])
def buscar_email_user(email):
    linha = buscar_user_por_email(email)

    if not linha:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    clientes = {
        "id": linha[0],
        "nome": linha[1],
        "cpf": linha[2],
        "email": linha[3],
        "telefone": linha[4],
        "correntista": linha[5],
        "score_credito": linha[6],
        "saldo_cc": linha[7],
        "admin": linha[8]
    }
    return jsonify(clientes), 200


@cliente_bp.route("/clientes/cpf/atualiza/<cpf>", methods=["PATCH"])
def atualizar_cliente_por_cpf(cpf):
    dados = request.get_json()

    linha = buscar_user_por_cpf(cpf)
    if not linha:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    id_cliente = linha[0]

    try:
        atualizar_user(
            id=id_cliente,
            nome=dados.get("nome"),
            cpf=dados.get("cpf"),
            email=dados.get("email"),
            telefone=dados.get("telefone"),
            correntista=dados.get("correntista"),
            score_credito=dados.get("score_credito"),
            saldo_cc=dados.get("saldo_cc")
        )
    except sqlite3.IntegrityError:
        return jsonify({"erro": "CPF, email ou telefone já cadastrados"}), 400

    return jsonify({"msg": "Atualizado com sucesso"}), 200


@cliente_bp.route("/clientes/delete/cpf/<cpf>", methods=["DELETE"])
def deletar_cliente_por_cpf(cpf):
    cliente = buscar_user_por_cpf(cpf)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    id_cliente = cliente[0]
    delete_user(id_cliente)
    return jsonify({"sucesso": "Cliente deletado"}), 200


@cliente_bp.route("/clientes/login", methods=["POST"])
def login_cliente():
    dados = request.get_json()

    cpf = dados.get("cpf")
    senha = dados.get("senha")

    if not cpf or not senha:
        return jsonify({"erro": "CPF e senha são obrigatórios"}), 400

    from ..repository.database import buscar_user_por_cpf_e_senha
    linha = buscar_user_por_cpf_e_senha(cpf, senha)

    if not linha:
        return jsonify({"erro": "CPF ou senha inválidos"}), 401

    return jsonify({
        "id": linha[0],
        "nome": linha[1],
        "cpf": linha[2],
        "email": linha[3],
        "telefone": linha[4],
        "correntista": linha[5],
        "score_credito": linha[6],
        "saldo_cc": linha[7],
        "admin": linha[8]
    }), 200

@cliente_bp.route("/clientes/alterar-senha", methods=["PATCH"])
def alterar_senha():
    dados = request.get_json()

    cpf = dados.get("cpf")
    senha_atual = dados.get("senha_atual")
    nova_senha = dados.get("nova_senha")

    if not cpf or not senha_atual or not nova_senha:
        return jsonify({"erro": "CPF, senha_atual e nova_senha são obrigatórios"}), 400

    from ..repository.database import buscar_user_por_cpf_e_senha
    cliente = buscar_user_por_cpf_e_senha(cpf, senha_atual)

    if not cliente:
        return jsonify({"erro": "Senha atual incorreta"}), 401

    id_cliente = cliente[0]

    atualizar_senha_por_id(id_cliente, nova_senha)

    return jsonify({"msg": "Senha alterada com sucesso"}), 200

import sqlite3
from flask import  Blueprint, request, jsonify
from ..repository.database import (
    listar_user, listar_investidores, listar_investimentos, listar_transacoes,
    buscar_user_por_id, buscar_investidor_por_id,
    buscar_investimento_por_id, buscar_cliente_com_investidor,
    atualizar_user, atualizar_investidor, atualizar_investimento, delete_user
)

adm_bp = Blueprint("admin", __name__)


@adm_bp.route("/admin/clientes/id/<cliente_id>", methods=["GET"])
def buscar_id_user(cliente_id):
    linha = buscar_user_por_id(cliente_id)

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

@adm_bp.route("/admin/investidor/cliente/<cliente_id>", methods=["GET"])
def buscar_investidor_e_cliente(cliente_id):
    linha = buscar_cliente_com_investidor(cliente_id)

    if not linha:
        return jsonify({"erro": "Investidor não encontrado"}), 404

    investidor = {
        "id": linha[0],
        "nome": linha[1],
        "cpf": linha[2],
        "email": linha[3],
        "telefone": linha[4],
        "correntista": linha[5],
        "score_credito": linha[6],
        "saldo_cc": linha[7],
        "admin": linha[8],
        "perfil_investidor": linha[9],
        "patrimonio_total": linha[10],
        "data_cadastro": linha[11],
    }

    return jsonify(investidor), 200
    
@adm_bp.route("/admin/investidor/id/<investidor_id>", methods=["GET"])
def buscar_investidor_id(investidor_id):
    linha = buscar_investidor_por_id(investidor_id)

    if not linha:
        return jsonify({"erro": "Investidor não encontrado"}), 404

    investidor = {
        "id_cliente": linha[0],
        "perfil_investidor": linha[1],
        "patrimonio_total": linha[2],
        "data_cadastro": linha[3]
    }
    return jsonify(investidor), 200


@adm_bp.route("/admin/clientes/id/<id>", methods=["PATCH"])
def atualizar(id):
    dados = request.get_json()
    linha = buscar_user_por_id(id)

    if not linha:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    try:
        atualizar_user(
            id=id,
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

    dados["id"] = id
    return jsonify(dados), 200

@adm_bp.route("/admin/investidor/id/atualiza/<id_cliente>", methods=["PATCH"])
def atualizar_investidor_por_id(id_cliente):
    dados = request.get_json()

    cliente = buscar_user_por_id(id_cliente)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    investidor = buscar_investidor_por_id(id_cliente)
    if not investidor:
        return jsonify({"erro": "Cliente não é investidor"}), 400

    try:
        atualizar_investidor(
            id_cliente=id_cliente,
            perfil_investidor=dados.get("perfil_investidor"),
            patrimonio_total=dados.get("patrimonio_total"),
            data_cadastro=dados.get("data_cadastro")
        )
    except sqlite3.IntegrityError:
        return jsonify({"erro": "Erro ao atualizar investidor"}), 400

    return jsonify({"msg": "Investidor atualizado com sucesso"}), 200

@adm_bp.route("/admin/investimentos/atualiza/<id_investimento>", methods=["PATCH"])
def atualizar_investimento_controller(id_investimento):
    dados = request.get_json()

    investimento = buscar_investimento_por_id(id_investimento)
    if not investimento:
        return jsonify({"erro": "Investimento não encontrado"}), 404

    try:
        atualizar_investimento(
            id_investimento=id_investimento,
            cliente_id=dados.get("cliente_id"),
            tipo_investimento=dados.get("tipo_investimento"),
            valor_investido=dados.get("valor_investido"),
            data_aplicacao=dados.get("data_aplicacao"),
            rentabilidade=dados.get("rentabilidade"),
            ativo=dados.get("ativo")
        )
    except sqlite3.IntegrityError:
        return jsonify({"erro": "Erro ao atualizar investidor"}), 400

    return jsonify({"msg": "Investimento atualizado com sucesso"}), 200

@adm_bp.route("/admin/clientes", methods=["GET"])
def listar_clientes():
    linhas = listar_user()
    lista = []

    for linha in linhas:
        lista.append({
            "id": linha[0],
            "nome": linha[1],
            "cpf": linha[2],
            "email": linha[3],
            "telefone": linha[4],
            "correntista": linha[5],
            "score_credito": linha[6],
            "saldo_cc": linha[7],
            "admin": linha[8]
        })

    return jsonify(lista), 200

@adm_bp.route("/admin/investidor", methods=["GET"])
def listar_investidor():
    linhas = listar_investidores()
    lista = []

    for linha in linhas:
        lista.append({
            "id_cliente": linha[0],
            "perfil_investidor": linha[1],
            "patrimonio_total": linha[2],
            "data_cadastro": linha[3], 
        })

    return jsonify(lista), 200

@adm_bp.route("/admin/investimentos", methods=["GET"])
def listar_investimentos_controller():
    linhas = listar_investimentos()
    lista = []

    for linha in linhas:
        lista.append({
            "id": linha[0],
            "cliente_id": linha[1],
            "tipo_investimento": linha[2],
            "valor_investido": linha[3],
            "data_aplicacao": linha[4],
            "rentabilidade": linha[5],
            "ativo": linha[6],
        })

    return jsonify(lista), 200


@adm_bp.route("/admin/transacoes/<id_cliente>", methods=["GET"])
def transacoes_listar(id_cliente):
    linhas = listar_transacoes(id_cliente)
    lista = []

    for linha in linhas:
        lista.append({
            "id_transacao": linha[0],
            "cliente_id": linha[1],
            "tipo": linha[2],
            "valor": linha[3],
            "data": linha[4],
            "descricao": linha[5]
        })

    return jsonify(lista), 200

@adm_bp.route("/admin/clientes/delete/id/<id>", methods=["DELETE"])
def deletar_cliente(id):
    linha = buscar_user_por_id(id)

    if not linha:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    delete_user(id)

    return jsonify({"sucesso": "Cliente deletado"}), 200


@adm_bp.route("/admin/investimento/id/<id_investimento>", methods=["GET"])
def buscar_investimento_por_id_controller(id_investimento):
    linha = buscar_investimento_por_id(id_investimento)

    if not linha:
        return jsonify({"erro": "Investimento não encontrado"}), 404

    return jsonify({
        "id_investimento": linha[0],
        "cliente_id": linha[1],
        "tipo_investimento": linha[2],
        "valor_investido": linha[3],
        "data_aplicacao": linha[4],
        "rentabilidade": linha[5],
        "ativo": linha[6]
    }), 200

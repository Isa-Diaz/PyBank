from flask import Blueprint, request, jsonify
from ..repository.database import (
    insert_investimento_api,
    listar_investimentos_api,
    buscar_investimento_api_por_id,
    atualizar_investimento_api,
    registrar_operacao_api,
    delete_investimento_api
)

invest_api_bp = Blueprint("invest_api", __name__)


@invest_api_bp.route("/api/acoes", methods=["POST"])
def criar_investimento_api():
    dados = request.get_json()

    cliente_id = dados.get("cliente_id")
    ticker = dados.get("ticker")
    quantidade = dados.get("quantidade")
    preco_unitario = dados.get("preco_unitario")
    custo_total = dados.get("custo_total")

    if not cliente_id:
        return jsonify({"erro": "cliente_id é obrigatório"}), 400

    id_invest = insert_investimento_api(
        cliente_id,
        ticker,
        quantidade,
        preco_unitario,
        custo_total
    )

    return jsonify({
        "msg": "Investimento de ação criado",
        "id_investimento": id_invest
    }), 201


@invest_api_bp.route("/api/acoes/cliente/<cliente_id>", methods=["GET"])
def listar_acoes_cliente(cliente_id):
    dados = listar_investimentos_api(cliente_id)
    lista = []

    for d in dados:
        lista.append({
            "id_investimento": d[0],
            "cliente_id": d[1],
            "ticker": d[2],
            "quantidade": d[3],
            "preco_unitario": d[4],
            "custo_total": d[5],
            "data": d[6]
        })

    return jsonify(lista), 200

@invest_api_bp.route("/api/acoes/<id_investimento>", methods=["GET"])
def buscar_invest_api(id_investimento):
    item = buscar_investimento_api_por_id(id_investimento)

    if not item:
        return jsonify({"erro": "Investimento não encontrado"}), 404

    return jsonify({
        "id_investimento": item[0],
        "cliente_id": item[1],
        "ticker": item[2],
        "quantidade": item[3],
        "preco_unitario": item[4],
        "custo_total": item[5],
        "data": item[6]
    }), 200

@invest_api_bp.route("/api/acoes/<id_investimento>", methods=["PATCH"])
def atualizar_invest_api(id_investimento):
    dados = request.get_json()

    nova_qtd = dados.get("quantidade")
    novo_custo = dados.get("custo_total")

    atualizar_investimento_api(id_investimento, nova_qtd, novo_custo)

    return jsonify({"msg": "Investimento atualizado"}), 200


@invest_api_bp.route("/api/acoes/transacao", methods=["POST"])
def registrar_operacao_api_controller():
    dados = request.get_json()

    registrar_operacao_api(
        dados["cliente_id"],
        dados["ticker"],
        dados["tipo"],
        dados["quantidade"],
        dados["preco_unitario"],
        dados["custo_total"]
    )

    return jsonify({"msg": "Operação registrada"}), 201



@invest_api_bp.route("/api/acoes/<id_investimento>", methods=["DELETE"])
def deletar_invest_api(id_investimento):
    delete_investimento_api(id_investimento)
    return jsonify({"msg": "Investimento excluído com sucesso"}), 200

from flask import Blueprint, request, jsonify
from ..service.service_stock import (
    comprar_acoes_service,
    vender_acoes_service,
    listar_acoes_cliente_service
)

stock_bp = Blueprint("stock_invest", __name__)


# ============================
# 1) COMPRA DE AÇÕES
# ============================
@stock_bp.route("/acoes/comprar", methods=["POST"])
def comprar_acoes_controller():
    dados = request.get_json()

    cpf = dados.get("cpf")
    ticker = dados.get("ticker")
    quantidade = dados.get("quantidade")
    valor_investir = dados.get("valor_investir")  # compra por valor

    resposta = comprar_acoes_service(
        cpf=cpf,
        ticker=ticker,
        quantidade=quantidade,
        valor_investir=valor_investir
    )

    return jsonify(resposta), 200


# ============================
# 2) VENDA DE AÇÕES
# ============================
@stock_bp.route("/acoes/vender", methods=["POST"])
def vender_acoes_controller():
    dados = request.get_json()

    cpf = dados.get("cpf")
    id_investimento = dados.get("id_investimento")
    quantidade = dados.get("quantidade")

    resposta = vender_acoes_service(
        cpf=cpf,
        id_investimento=id_investimento,
        quantidade=quantidade
    )

    return jsonify(resposta), 200

@stock_bp.route("/acoes/cliente/<cpf>", methods=["GET"])
def listar_acoes_cliente_controller(cpf):

    from ..service.service_stock import listar_acoes_cliente_service

    resposta = listar_acoes_cliente_service(cpf)

    return jsonify(resposta), 200

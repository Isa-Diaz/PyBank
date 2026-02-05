from flask import Blueprint, jsonify
from ..service.service_api import (
    analise_mercado_service,
    analise_carteira_service,
    projecao_retorno_service
)

invest_api_bp = Blueprint("invest_api", __name__)

@invest_api_bp.route("/analises/mercado/<ticker>", methods=["GET"])
def analisar_mercado_controller(ticker):

    resposta = analise_mercado_service(ticker)

    if "erro" in resposta:
        return jsonify(resposta), 400

    return jsonify(resposta), 200


@invest_api_bp.route("/analises/carteira/<cpf>", methods=["GET"])
def analisar_carteira_controller(cpf):
    resposta = analise_carteira_service(cpf)
    return jsonify(resposta), 200


@invest_api_bp.route("/calculos/projecao/<cpf>", methods=["GET"])
def projecao_retorno_controller(cpf):
    resposta = projecao_retorno_service(cpf)
    return jsonify(resposta), 200


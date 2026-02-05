from flask import Blueprint, request, jsonify
from ..service.service_invest import (
    criar_investidor_service,
    criar_investimento_fixo_service,
    listar_investimentos_service,
    patrimonio_service,
    deletar_investimento_service,
    aporte_service, resgate_service
)

invest_fixo_bp = Blueprint("investimentos_fixo", __name__)


@invest_fixo_bp.route("/investidor", methods=["POST"])
def criar_investidor_controller():
    dados = request.get_json()

    cpf = dados.get("cpf")
    perfil = dados.get("perfil_investidor")
    patrimonio_inicial = dados.get("patrimonio_inicial")

    resposta = criar_investidor_service(cpf, perfil, patrimonio_inicial)

    if "erro" in resposta:
        if resposta["erro"] == "Cliente já é investidor":
            return jsonify(resposta), 409
        return jsonify(resposta), 400

    return jsonify(resposta), 201



@invest_fixo_bp.route("/investimentos/fixo", methods=["POST"])
def criar_investimento_fixo_controller():

    dados = request.get_json()

    cpf = dados.get("cpf")
    valor = dados.get("valor_investido")

    resposta = criar_investimento_fixo_service(cpf, valor)
    return jsonify(resposta), 200


@invest_fixo_bp.route("/investimentos/<cpf>", methods=["GET"])
def listar_investimentos_controller(cpf):

    resposta = listar_investimentos_service(cpf)
    return jsonify(resposta), 200

@invest_fixo_bp.route("/patrimonio/<cpf>", methods=["GET"])
def patrimonio_controller(cpf):

    resposta = patrimonio_service(cpf)
    return jsonify(resposta), 200

@invest_fixo_bp.route("/investimentos/<id_investimento>", methods=["DELETE"])
def deletar_investimento_controller(id_investimento):
    return jsonify(deletar_investimento_service(id_investimento)), 200

@invest_fixo_bp.route("/investimentos/aporte/<id_investimento>", methods=["POST"])
def aporte_controller(id_investimento):
    dados = request.get_json()

    cpf = dados.get("cpf")
    valor = dados.get("valor")

    return jsonify(aporte_service(cpf, id_investimento, valor)), 200



# ✅ RESGATE
@invest_fixo_bp.route("/investimentos/resgate/<id_investimento>", methods=["POST"])
def resgate_controller(id_investimento):
    dados = request.get_json()

    cpf = dados.get("cpf")
    valor = dados.get("valor")

    return jsonify(resgate_service(cpf, id_investimento, valor)), 200
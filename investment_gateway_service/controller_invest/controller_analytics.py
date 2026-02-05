from flask import Blueprint, jsonify
from ..service.service_analytics import performance_carteira_service

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics/carteira/<cpf>", methods=["GET"])
def analytics_carteira_controller(cpf):
    resposta = performance_carteira_service(cpf)
    return jsonify(resposta), 200

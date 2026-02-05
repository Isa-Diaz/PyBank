from flask import Blueprint
from ..service.service_graphics import grafico_preco_service, grafico_projecao_service

graphics_bp = Blueprint("graphics", __name__)

@graphics_bp.route("/graficos/preco/<ticker>", methods=["GET"])
def grafico_preco_controller(ticker):
    return grafico_preco_service(ticker)

@graphics_bp.route("/graficos/projecao/<ticker>", methods=["GET"])
def grafico_projecao_controller(ticker):
    return grafico_projecao_service(ticker)
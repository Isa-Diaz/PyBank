import requests
from .core import URL_MS1, resposta


def criar_investidor_ms1(id_cliente, dados):
    return resposta(requests.post(
        f"{URL_MS1}/admin/investidor/{id_cliente}",
        json=dados
    ))


def atualizar_investidor_ms1(id_cliente, dados):
    return resposta(requests.patch(
        f"{URL_MS1}/admin/investidor/id/atualiza/{id_cliente}",
        json=dados
    ))


def buscar_cliente_por_cpf_ms1(cpf):
    return resposta(requests.get(
        f"{URL_MS1}/clientes/buscar/cpf/{cpf}"
    ))


def criar_investimento_ms1(dados):
    return resposta(requests.post(
        f"{URL_MS1}/admin/investimentos",
        json=dados
    ))


def listar_investimentos_cliente_ms1(id_cliente):
    return resposta(requests.get(
        f"{URL_MS1}/admin/investimentos/{id_cliente}"
    ))


def listar_todos_investimentos_ms1():
    return resposta(requests.get(
        f"{URL_MS1}/admin/investimentos"
    ))


def buscar_investidor_ms1(id_cliente):
    return resposta(requests.get(
        f"{URL_MS1}/admin/investidor/{id_cliente}"
    ))


def atualizar_investimento_ms1(id_investimento, dados):
    return resposta(requests.patch(
        f"{URL_MS1}/admin/investimentos/{id_investimento}",
        json=dados
    ))


def buscar_investimento_ms1(id_investimento):
    return resposta(requests.get(
        f"{URL_MS1}/admin/investimento/id/{id_investimento}"
    ))


def buscar_cliente_por_id_ms1(id_cliente):
    return resposta(requests.get(
        f"{URL_MS1}/admin/clientes/id/{id_cliente}"
    ))


def deletar_investimento_ms1(id_investimento):
    return resposta(requests.delete(
        f"{URL_MS1}/admin/investimentos/{id_investimento}"
    ))

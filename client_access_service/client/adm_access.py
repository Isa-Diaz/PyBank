from .core import URL, resposta
import requests

def listar_clientes():
    return resposta(requests.get(f"{URL}/admin/clientes"))

def buscar_cliente_por_id(id):
    return resposta(requests.get(f"{URL}/admin/clientes/id/{id}"))

def atualizar_cliente(id, dados):
    return resposta(requests.patch(f"{URL}/admin/clientes/id/{id}", json=dados))

def listar_investidores():
    return resposta(requests.get(f"{URL}/admin/investidor"))

def buscar_investidor_por_id(id_cliente):
    return resposta(requests.get(f"{URL}/admin/investidor/id/{id_cliente}"))

def buscar_investidor_com_cliente(id_cliente):
    return resposta(requests.get(f"{URL}/admin/investidor/cliente/{id_cliente}"))

def listar_transacoes_por_id(id_cliente):
    return resposta(requests.get(f"{URL}/admin/transacoes/{id_cliente}"))

def deletar_cliente(id):
    return resposta(requests.delete(f"{URL}/admin/clientes/delete/id/{id}"))

def listar_investimentos():
    return resposta(requests.get(f"{URL}/admin/investimentos"))

def listar_investimentos_por_cliente(id_cliente):
    return resposta(requests.get(f"{URL}/admin/investimentos/{id_cliente}"))

def deletar_cliente_por_id(id_cliente):
    try:
        return requests.delete(
            f"{URL}/admin/clientes/delete/id/{id_cliente}",
            timeout=5
        )
    except requests.RequestException:
        return None

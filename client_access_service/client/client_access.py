import requests

MS1_URL = "http://localhost:5000"


def buscar_cliente_por_cpf(cpf: str):
    try:
        return requests.get(f"{MS1_URL}/clientes/buscar/cpf/{cpf}", timeout=5)
    except requests.RequestException:
        return None


def criar_cliente(dados: dict):
    try:
        return requests.post(f"{MS1_URL}/clientes", json=dados, timeout=5)
    except requests.RequestException:
        return None


def atualizar_cliente_por_cpf(cpf: str, dados: dict):
    try:
        return requests.patch(f"{MS1_URL}/clientes/cpf/atualiza/{cpf}", json=dados, timeout=5)
    except requests.RequestException:
        return None


def buscar_user_por_email(email: str):
    try:
        return requests.get(f"{MS1_URL}/clientes/buscar/email/{email}", timeout=5)
    except requests.RequestException:
        return None


def buscar_user_telefone(telefone: str):
    try:
        return requests.get(f"{MS1_URL}/clientes/buscar/telefone/{telefone}", timeout=5)
    except requests.RequestException:
        return None


def criar_transacao(dados: dict):
    try:
        return requests.post(f"{MS1_URL}/clientes/transacao", json=dados, timeout=5)
    except requests.RequestException:
        return None


def login_ms1(cpf, senha):
    try:
        return requests.post(
            f"{MS1_URL}/clientes/login",
            json={"cpf": cpf, "senha": senha},
            timeout=5
        )
    except requests.RequestException:
        return None


def alterar_senha_ms1(cpf, senha_atual, nova_senha):
    try:
        return requests.patch(
            f"{MS1_URL}/clientes/alterar-senha",
            json={
                "cpf": cpf,
                "senha_atual": senha_atual,
                "nova_senha": nova_senha
            },
            timeout=5
        )
    except requests.RequestException:
        return None

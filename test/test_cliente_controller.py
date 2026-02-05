import pytest
from unittest.mock import patch
from investment_data_service.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ---------------------------------------------------------
# POST /clientes  (criar cliente)
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.cliente_controller.insert_user")
def test_criar_cliente_ok(mock_insert, client):
    mock_insert.return_value = "123"

    payload = {
        "nome": "Joao",
        "cpf": "12345678901",
        "email": "j@a.com",
        "telefone": "11999999999",
        "correntista": 1,
        "score_credito": 700,
        "saldo_cc": 1000,
        "admin": 0,
        "senha": "123"
    }

    resp = client.post("/clientes", json=payload)
    assert resp.status_code == 201
    assert resp.get_json()["id"] == "123"


@patch("investment_data_service.controller_storage.cliente_controller.insert_user")
def test_criar_cliente_integrity_error(mock_insert, client):
    import sqlite3
    mock_insert.side_effect = sqlite3.IntegrityError()

    resp = client.post("/clientes", json={"cpf": "1"})
    assert resp.status_code == 400


# ---------------------------------------------------------
# POST /clientes/transacao
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.cliente_controller.insert_transacao")
def test_criar_transacao_ok(mock_insert, client):
    mock_insert.return_value = 10

    payload = {
        "cliente_id": "1",
        "tipo": "deposito",
        "valor": 100,
        "descricao": "teste"
    }

    resp = client.post("/clientes/transacao", json=payload)
    assert resp.status_code == 201
    assert resp.get_json()["id_transacao"] == 10


def test_criar_transacao_campos_faltando(client):
    resp = client.post("/clientes/transacao", json={})
    assert resp.status_code == 400


@patch("investment_data_service.controller_storage.cliente_controller.insert_transacao")
def test_criar_transacao_integrity_error(mock_insert, client):
    import sqlite3
    mock_insert.side_effect = sqlite3.IntegrityError()

    resp = client.post("/clientes/transacao", json={
        "cliente_id": "1",
        "tipo": "deposito",
        "valor": 10
    })
    assert resp.status_code == 400


# ---------------------------------------------------------
# GET buscar por CPF
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.cliente_controller.buscar_user_por_cpf")
def test_buscar_cpf_ok(mock_buscar, client):
    mock_buscar.return_value = (
        "1","Joao","123","j@a.com","119",1,700,1000,0
    )

    resp = client.get("/clientes/buscar/cpf/123")
    assert resp.status_code == 200
    assert resp.get_json()["cpf"] == "123"


@patch("investment_data_service.controller_storage.cliente_controller.buscar_user_por_cpf")
def test_buscar_cpf_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.get("/clientes/buscar/cpf/123")
    assert resp.status_code == 404


# ---------------------------------------------------------
# GET buscar por telefone
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.cliente_controller.buscar_user_por_telefone")
def test_buscar_telefone_ok(mock_buscar, client):
    mock_buscar.return_value = (
        "1","Joao","123","j@a.com","119",1,700,1000,0
    )
    resp = client.get("/clientes/buscar/telefone/119")
    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.cliente_controller.buscar_user_por_telefone")
def test_buscar_telefone_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.get("/clientes/buscar/telefone/119")
    assert resp.status_code == 404


# ---------------------------------------------------------
# GET buscar por email
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.cliente_controller.buscar_user_por_email")
def test_buscar_email_ok(mock_buscar, client):
    mock_buscar.return_value = (
        "1","Joao","123","j@a.com","119",1,700,1000,0
    )
    resp = client.get("/clientes/buscar/email/j@a.com")
    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.cliente_controller.buscar_user_por_email")
def test_buscar_email_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.get("/clientes/buscar/email/x@x.com")
    assert resp.status_code == 404


# ---------------------------------------------------------
# PATCH atualizar por CPF
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.cliente_controller.atualizar_user")
@patch("investment_data_service.controller_storage.cliente_controller.buscar_user_por_cpf")
def test_atualizar_por_cpf_ok(mock_buscar, mock_atualizar, client):
    mock_buscar.return_value = ("1",)

    resp = client.patch("/clientes/cpf/atualiza/123", json={"nome": "Novo"})
    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.cliente_controller.buscar_user_por_cpf")
def test_atualizar_por_cpf_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.patch("/clientes/cpf/atualiza/123", json={"nome": "Novo"})
    assert resp.status_code == 404


@patch("investment_data_service.controller_storage.cliente_controller.atualizar_user")
@patch("investment_data_service.controller_storage.cliente_controller.buscar_user_por_cpf")
def test_atualizar_por_cpf_integrity_error(mock_buscar, mock_update, client):
    import sqlite3
    mock_buscar.return_value = ("1",)
    mock_update.side_effect = sqlite3.IntegrityError()

    resp = client.patch("/clientes/cpf/atualiza/123", json={"cpf": "X"})
    assert resp.status_code == 400


# ---------------------------------------------------------
# DELETE por CPF
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.cliente_controller.delete_user")
@patch("investment_data_service.controller_storage.cliente_controller.buscar_user_por_cpf")
def test_deletar_por_cpf_ok(mock_buscar, mock_delete, client):
    mock_buscar.return_value = ("1",)
    resp = client.delete("/clientes/delete/cpf/123")
    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.cliente_controller.buscar_user_por_cpf")
def test_deletar_por_cpf_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.delete("/clientes/delete/cpf/123")
    assert resp.status_code == 404



# ---------------------------------------------------------
# POST login
# ---------------------------------------------------------

@patch("investment_data_service.repository.database.buscar_user_por_cpf_e_senha")
def test_login_ok(mock_buscar, client):
    mock_buscar.return_value = (
        "1","Joao","123","j@a.com","119",1,700,1000,0
    )
    resp = client.post("/clientes/login", json={"cpf": "123", "senha": "abc"})
    assert resp.status_code == 200


def test_login_faltando_campos(client):
    resp = client.post("/clientes/login", json={})
    assert resp.status_code == 400


@patch("investment_data_service.repository.database.buscar_user_por_cpf_e_senha")
def test_login_401(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.post("/clientes/login", json={"cpf": "123", "senha": "abc"})
    assert resp.status_code == 401


# ---------------------------------------------------------
# PATCH alterar senha
# ---------------------------------------------------------
@patch("investment_data_service.repository.database.atualizar_senha_por_id")
@patch("investment_data_service.repository.database.buscar_user_por_cpf_e_senha")
def test_alterar_senha_ok(mock_buscar, mock_update, client):
    mock_buscar.return_value = ("1",)
    resp = client.patch("/clientes/alterar-senha", json={
        "cpf": "123",
        "senha_atual": "abc",
        "nova_senha": "xyz"
    })
    assert resp.status_code == 200


def test_alterar_senha_faltando_campos(client):
    resp = client.patch("/clientes/alterar-senha", json={})
    assert resp.status_code == 400


@patch("investment_data_service.repository.database.buscar_user_por_cpf_e_senha")
def test_alterar_senha_401(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.patch("/clientes/alterar-senha", json={
        "cpf": "123",
        "senha_atual": "abc",
        "nova_senha": "xyz"
    })
    assert resp.status_code == 401



# ---------------------------------------------------------
# PATCH alterar senha
# ---------------------------------------------------------

@patch("investment_data_service.repository.database.atualizar_senha_por_id")


@patch("investment_data_service.repository.database.buscar_user_por_cpf_e_senha")

def test_alterar_senha_ok(mock_buscar, mock_update, client):
    mock_buscar.return_value = ("1",)

    resp = client.patch("/clientes/alterar-senha", json={
        "cpf": "123",
        "senha_atual": "abc",
        "nova_senha": "xyz"
    })

    assert resp.status_code == 200


def test_alterar_senha_faltando_campos(client):
    resp = client.patch("/clientes/alterar-senha", json={})
    assert resp.status_code == 400



@patch("investment_data_service.repository.database.buscar_user_por_cpf_e_senha")
def test_alterar_senha_401(mock_buscar, client):
    mock_buscar.return_value = None

    resp = client.patch("/clientes/alterar-senha", json={
        "cpf": "123",
        "senha_atual": "abc",
        "nova_senha": "xyz"
    })

    assert resp.status_code == 401

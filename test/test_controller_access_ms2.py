from unittest.mock import patch
import pytest


# ===========================
#       CLIENTE
# ===========================

@patch("client_access_service.controller.controller_access.criar_cliente_service")
def test_criar_cliente_controller_ok(mock_service, client):
    mock_service.return_value = ({"msg": "ok"}, 200)

    resp = client.post("/cliente", json={
        "nome": "Joao",
        "cpf": "12345678901",
        "email": "j@a.com",
        "telefone": "11999999999",
        "correntista": True,
        "saldo_cc": 100,
        "senha": "123"
    })

    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.buscar_cliente_service")
def test_buscar_cliente_controller_ok(mock_service, client):
    mock_service.return_value = ({"id": "1"}, 200)
    resp = client.get("/cliente/12345678901")
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.atualizar_cliente_service")
def test_atualizar_cliente_controller_ok(mock_service, client):
    mock_service.return_value = ({"msg": "atualizado"}, 200)
    resp = client.patch("/cliente/12345678901", json={"nome": "Novo"})
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.deletar_cliente_service")
def test_deletar_cliente_controller_ok(mock_service, client):
    mock_service.return_value = ({"msg": "apagado"}, 200)
    resp = client.delete("/cliente/12345678901")
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.operacao_service")
def test_operacao_cliente_controller_ok(mock_service, client):
    mock_service.return_value = ({"msg": "ok"}, 200)
    resp = client.post("/cliente/operacao/12345678901", json={"tipo": "deposito", "valor": 10})
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.listar_transacoes_cpf")
def test_listar_transacoes_controller_ok(mock_service, client):
    mock_service.return_value = ([], 200)
    resp = client.get("/cliente/transacoes/12345678901")
    assert resp.status_code == 200


# ===========================
#           ADMIN
# ===========================

@patch("client_access_service.controller.controller_access.listar_todos_clientes_service")
def test_admin_listar_clientes_ok(mock_service, client):
    mock_service.return_value = ([], 200)
    resp = client.get("/admin/clientes")
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.buscar_cliente_admin_service")
def test_admin_buscar_cliente_ok(mock_service, client):
    mock_service.return_value = ({"id": "1"}, 200)
    resp = client.get("/admin/clientes/1")
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.atualizar_cliente_admin_service")
def test_admin_atualizar_cliente_ok(mock_service, client):
    mock_service.return_value = ({"msg": "ok"}, 200)
    resp = client.patch("/admin/clientes/1", json={"nome": "Novo"})
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.deletar_cliente_admin_service")
def test_admin_deletar_cliente_ok(mock_service, client):
    mock_service.return_value = ({"msg": "ok"}, 200)
    resp = client.delete("/admin/clientes/1")
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.listar_transacoes_admin_service")
def test_admin_listar_transacoes_ok(mock_service, client):
    mock_service.return_value = ([], 200)
    resp = client.get("/admin/transacoes/1")
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.listar_todos_investidores_service")
def test_admin_listar_investidores_ok(mock_service, client):
    mock_service.return_value = ([], 200)
    resp = client.get("/admin/investidores")
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.buscar_investidor_admin_service")
def test_admin_buscar_investidor_ok(mock_service, client):
    mock_service.return_value = ({"perfil": "moderado"}, 200)
    resp = client.get("/admin/investidor/1")
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.buscar_cliente_com_investidor_service")
def test_admin_buscar_cliente_com_investidor_ok(mock_service, client):
    mock_service.return_value = ({"nome": "Joao"}, 200)
    resp = client.get("/admin/cliente-investidor/1")
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.promover_para_admin")
def test_admin_promover_ok(mock_service, client):
    mock_service.return_value = ({"msg": "promovido"}, 200)
    resp = client.post("/admin/promover/1")
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.remover_admin")
def test_admin_remover_ok(mock_service, client):
    mock_service.return_value = ({"msg": "removido"}, 200)
    resp = client.post("/admin/remover/1")
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.alterar_cpf_admin_service")
def test_admin_alterar_cpf_ok(mock_service, client):
    mock_service.return_value = ({"msg": "cpf alterado"}, 200)
    resp = client.post("/admin/alterar-cpf/1", json={"novo_cpf": "12345678901"})
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.listar_clientes_com_investimentos_service")
def test_admin_listar_clientes_com_investimentos_ok(mock_service, client):
    mock_service.return_value = ([], 200)
    resp = client.get("/admin/clientes/investimentos")
    assert resp.status_code == 200


# ===========================
#     LOGIN / SENHA
# ===========================

@patch("client_access_service.controller.controller_access.login_service")
def test_login_ok(mock_service, client):
    mock_service.return_value = ({"id": "1"}, 200)
    resp = client.post("/login", json={"cpf": "123", "senha": "abc"})
    assert resp.status_code == 200


@patch("client_access_service.controller.controller_access.alterar_senha_service")
def test_alterar_senha_ok(mock_service, client):
    mock_service.return_value = ({"msg": "ok"}, 200)
    resp = client.patch("/alterar-senha", json={"cpf": "123", "senha_atual": "x", "nova_senha": "y"})
    assert resp.status_code == 200

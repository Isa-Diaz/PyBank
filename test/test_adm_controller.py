import json
import pytest
from unittest.mock import patch

# IMPORT CORRETO DO BLUEPRINT VIA APP
from investment_data_service.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# -------------------------------
# TESTE: /admin/clientes/id/<id>
# -------------------------------
@patch("investment_data_service.controller_storage.adm_controller.buscar_user_por_id")
def test_buscar_id_user_ok(mock_buscar, client):
    mock_buscar.return_value = (
        "1", "João", "12345678901", "j@a.com", "11999999999",
        1, 700, 1000, 0
    )

    resp = client.get("/admin/clientes/id/1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == "1"
    assert data["nome"] == "João"


@patch("investment_data_service.controller_storage.adm_controller.buscar_user_por_id")
def test_buscar_id_user_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.get("/admin/clientes/id/1")
    assert resp.status_code == 404


# ----------------------------------------------
# TESTE: /admin/investidor/cliente/<cliente_id>
# ----------------------------------------------
@patch("investment_data_service.controller_storage.adm_controller.buscar_cliente_com_investidor")
def test_buscar_investidor_e_cliente_ok(mock_buscar, client):
    mock_buscar.return_value = (
        "1", "João", "123", "j@a.com", "119", 1, 700, 1000, 0,
        "moderado", 20000, "2024-01-01"
    )

    resp = client.get("/admin/investidor/cliente/1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["perfil_investidor"] == "moderado"


@patch("investment_data_service.controller_storage.adm_controller.buscar_cliente_com_investidor")
def test_buscar_investidor_e_cliente_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.get("/admin/investidor/cliente/1")
    assert resp.status_code == 404


# ----------------------------------------------
# TESTE: /admin/investidor/id/<id>
# ----------------------------------------------
@patch("investment_data_service.controller_storage.adm_controller.buscar_investidor_por_id")
def test_buscar_investidor_id_ok(mock_buscar, client):
    mock_buscar.return_value = ("1", "moderado", 10000, "2024-01-01")

    resp = client.get("/admin/investidor/id/1")
    assert resp.status_code == 200
    assert resp.get_json()["perfil_investidor"] == "moderado"


@patch("investment_data_service.controller_storage.adm_controller.buscar_investidor_por_id")
def test_buscar_investidor_id_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.get("/admin/investidor/id/1")
    assert resp.status_code == 404


# ----------------------------------------------
# PATCH /admin/clientes/id/<id>
# ----------------------------------------------
@patch("investment_data_service.controller_storage.adm_controller.atualizar_user")
@patch("investment_data_service.controller_storage.adm_controller.buscar_user_por_id")
def test_atualizar_cliente_ok(mock_buscar, mock_update, client):
    mock_buscar.return_value = ("1",)
    payload = {"nome": "Novo Nome"}

    resp = client.patch("/admin/clientes/id/1", json=payload)
    assert resp.status_code == 200
    assert resp.get_json()["nome"] == "Novo Nome"


@patch("investment_data_service.controller_storage.adm_controller.buscar_user_por_id")
def test_atualizar_cliente_404(mock_buscar, client):
    mock_buscar.return_value = None

    resp = client.patch("/admin/clientes/id/1", json={"nome": "X"})
    assert resp.status_code == 404


@patch("investment_data_service.controller_storage.adm_controller.atualizar_user")
@patch("investment_data_service.controller_storage.adm_controller.buscar_user_por_id")
def test_atualizar_cliente_integrity_error(mock_buscar, mock_update, client):
    mock_buscar.return_value = ("1",)

    import sqlite3
    mock_update.side_effect = sqlite3.IntegrityError()

    resp = client.patch("/admin/clientes/id/1", json={"cpf": "111"})
    assert resp.status_code == 400


# ---------------------------------------------------------
# PATCH /admin/investidor/id/atualiza/<id_cliente>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.adm_controller.atualizar_investidor")
@patch("investment_data_service.controller_storage.adm_controller.buscar_investidor_por_id")
@patch("investment_data_service.controller_storage.adm_controller.buscar_user_por_id")
def test_atualizar_investidor_ok(mock_user, mock_inv, mock_update, client):
    mock_user.return_value = ("1",)
    mock_inv.return_value = ("1",)

    resp = client.patch("/admin/investidor/id/atualiza/1", json={
        "perfil_investidor": "arrojado"
    })

    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.adm_controller.buscar_user_por_id")
def test_atualizar_investidor_cliente_404(mock_user, client):
    mock_user.return_value = None
    resp = client.patch("/admin/investidor/id/atualiza/1", json={})
    assert resp.status_code == 404


@patch("investment_data_service.controller_storage.adm_controller.buscar_user_por_id")
@patch("investment_data_service.controller_storage.adm_controller.buscar_investidor_por_id")
def test_atualizar_investidor_400(mock_inv, mock_user, client):
    mock_user.return_value = ("1",)
    mock_inv.return_value = None

    resp = client.patch("/admin/investidor/id/atualiza/1", json={})
    assert resp.status_code == 400


# ---------------------------------------------------------
# GET /admin/investimentos
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.adm_controller.listar_investimentos")
def test_listar_investimentos(mock_list, client):
    mock_list.return_value = [
        (1, "1", "CDB", 1000, "2024-01-01", 0.12, 1)
    ]

    resp = client.get("/admin/investimentos")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


# ---------------------------------------------------------
# GET /admin/transacoes/<id_cliente>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.adm_controller.listar_transacoes")
def test_transacoes_listar(mock_list, client):
    mock_list.return_value = [
        (1, "1", "deposito", 100, "2024-01-01", "teste")
    ]

    resp = client.get("/admin/transacoes/1")
    assert resp.status_code == 200


# ---------------------------------------------------------
# DELETE /admin/clientes/delete/id/<id>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.adm_controller.delete_user")
@patch("investment_data_service.controller_storage.adm_controller.buscar_user_por_id")
def test_deletar_cliente_ok(mock_buscar, mock_del, client):
    mock_buscar.return_value = ("1",)

    resp = client.delete("/admin/clientes/delete/id/1")
    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.adm_controller.buscar_user_por_id")
def test_deletar_cliente_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.delete("/admin/clientes/delete/id/1")
    assert resp.status_code == 404

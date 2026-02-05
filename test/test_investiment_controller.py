import pytest
from unittest.mock import patch
from investment_data_service.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ---------------------------------------------------------
# POST /admin/investidor/<id_cliente>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.investiment_controller.insert_investidor")
@patch("investment_data_service.controller_storage.investiment_controller.buscar_investidor_por_id")
@patch("investment_data_service.controller_storage.investiment_controller.buscar_user_por_id")
def test_criar_investidor_ok(mock_user, mock_inv, mock_insert, client):
    mock_user.return_value = ("1",)
    mock_inv.return_value = None
    mock_insert.return_value = "1"

    resp = client.post("/admin/investidor/1", json={
        "perfil_investidor": "moderado",
        "patrimonio_total": 10000,
        "data_cadastro": "2024-01-01"
    })

    assert resp.status_code == 201


@patch("investment_data_service.controller_storage.investiment_controller.buscar_user_por_id")
def test_criar_investidor_cliente_404(mock_user, client):
    mock_user.return_value = None
    resp = client.post("/admin/investidor/1", json={})
    assert resp.status_code == 404


@patch("investment_data_service.controller_storage.investiment_controller.buscar_investidor_por_id")
@patch("investment_data_service.controller_storage.investiment_controller.buscar_user_por_id")
def test_criar_investidor_400(mock_user, mock_inv, client):
    mock_user.return_value = ("1",)
    mock_inv.return_value = ("1",)  # Já é investidor

    resp = client.post("/admin/investidor/1", json={})
    assert resp.status_code == 400


# ---------------------------------------------------------
# POST /admin/investimentos
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.investiment_controller.insert_tipo_investimento")
@patch("investment_data_service.controller_storage.investiment_controller.buscar_user_por_id")
def test_criar_investimento_ok(mock_user, mock_insert, client):
    mock_user.return_value = ("1",)
    mock_insert.return_value = (10, "1")

    resp = client.post("/admin/investimentos", json={
        "cliente_id": "1",
        "tipo_investimento": "CDB",
        "valor_investido": 1000,
        "data_aplicacao": "2024-01-01",
        "rentabilidade": 0.12,
        "ativo": 1
    })

    assert resp.status_code == 201
    assert resp.get_json()["id_investimento"] == 10


@patch("investment_data_service.controller_storage.investiment_controller.buscar_user_por_id")
def test_criar_investimento_cliente_404(mock_user, client):
    mock_user.return_value = None
    resp = client.post("/admin/investimentos", json={})
    assert resp.status_code == 404


# ---------------------------------------------------------
# GET /admin/investimentos/<id_cliente>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.investiment_controller.listar_investimentos")
def test_listar_investimentos_cliente(mock_list, client):
    mock_list.return_value = [
        (1, "1", "CDB", 1000, "2024-01-01", 0.12, 1),
        (2, "2", "LCI", 2000, "2024-02-01", 0.10, 1),
    ]

    resp = client.get("/admin/investimentos/1")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


# ---------------------------------------------------------
# GET /admin/investidor/<id_cliente>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.investiment_controller.buscar_investidor_por_id")
def test_buscar_investidor_ok(mock_buscar, client):
    mock_buscar.return_value = ("1", "moderado", 10000, "2024-01-01")

    resp = client.get("/admin/investidor/1")
    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.investiment_controller.buscar_investidor_por_id")
def test_buscar_investidor_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.get("/admin/investidor/1")
    assert resp.status_code == 404


# ---------------------------------------------------------
# GET /admin/investimentos
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.investiment_controller.listar_investimentos")
def test_listar_todos_investimentos(mock_list, client):
    mock_list.return_value = [
        (1, "1", "CDB", 1000, "2024-01-01", 0.12, 1)
    ]
    resp = client.get("/admin/investimentos")
    assert resp.status_code == 200


# ---------------------------------------------------------
# PATCH /admin/investimentos/<id_investimento>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.investiment_controller.atualizar_investimento")
@patch("investment_data_service.controller_storage.investiment_controller.buscar_investimento_por_id")
def test_atualizar_investimento_ok(mock_buscar, mock_update, client):
    mock_buscar.return_value = ("1", "1", "CDB", 1000, "2024-01-01", 0.12, 1)

    resp = client.patch("/admin/investimentos/1", json={
        "valor_investido": 2000
    })

    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.investiment_controller.buscar_investimento_por_id")
def test_atualizar_investimento_404(mock_buscar, client):
    mock_buscar.return_value = None

    resp = client.patch("/admin/investimentos/1", json={})
    assert resp.status_code == 404


# ---------------------------------------------------------
# DELETE /admin/investimentos/<id_investimento>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.investiment_controller.delete_investimento")
@patch("investment_data_service.controller_storage.investiment_controller.buscar_investimento_por_id")
def test_deletar_investimento_ok(mock_buscar, mock_delete, client):
    mock_buscar.return_value = ("1",)

    resp = client.delete("/admin/investimentos/1")
    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.investiment_controller.buscar_investimento_por_id")
def test_deletar_investimento_404(mock_buscar, client):
    mock_buscar.return_value = None

    resp = client.delete("/admin/investimentos/1")
    assert resp.status_code == 404

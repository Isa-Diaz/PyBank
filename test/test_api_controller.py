import pytest
from unittest.mock import patch
from investment_data_service.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ---------------------------------------------------------
# POST /api/acoes
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.api_controller.insert_investimento_api")
def test_criar_investimento_api_ok(mock_insert, client):
    mock_insert.return_value = 10

    payload = {
        "cliente_id": "1",
        "ticker": "PETR4",
        "quantidade": 10,
        "preco_unitario": 30,
        "custo_total": 300
    }

    resp = client.post("/api/acoes", json=payload)
    assert resp.status_code == 201
    assert resp.get_json()["id_investimento"] == 10


def test_criar_investimento_api_erro(client):
    # cliente_id ausente
    payload = {
        "ticker": "PETR4"
    }
    resp = client.post("/api/acoes", json=payload)
    assert resp.status_code == 400


# ---------------------------------------------------------
# GET /api/acoes/cliente/<cliente_id>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.api_controller.listar_investimentos_api")
def test_listar_acoes_cliente(mock_list, client):
    mock_list.return_value = [
        (1, "1", "PETR4", 10, 30, 300, "2024-01-01")
    ]

    resp = client.get("/api/acoes/cliente/1")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


# ---------------------------------------------------------
# GET /api/acoes/<id_investimento>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.api_controller.buscar_investimento_api_por_id")
def test_buscar_invest_api_ok(mock_buscar, client):
    mock_buscar.return_value = (1, "1", "PETR4", 10, 30, 300, "2024-01-01")

    resp = client.get("/api/acoes/1")
    assert resp.status_code == 200
    assert resp.get_json()["ticker"] == "PETR4"


@patch("investment_data_service.controller_storage.api_controller.buscar_investimento_api_por_id")
def test_buscar_invest_api_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.get("/api/acoes/1")
    assert resp.status_code == 404


# ---------------------------------------------------------
# PATCH /api/acoes/<id_investimento>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.api_controller.atualizar_investimento_api")
def test_atualizar_invest_api_ok(mock_update, client):
    payload = {"quantidade": 20, "custo_total": 600}

    resp = client.patch("/api/acoes/1", json=payload)
    assert resp.status_code == 200
    assert resp.get_json()["msg"] == "Investimento atualizado"


# ---------------------------------------------------------
# POST /api/acoes/transacao
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.api_controller.registrar_operacao_api")
def test_registrar_operacao_api(mock_registrar, client):
    payload = {
        "cliente_id": "1",
        "ticker": "PETR4",
        "tipo": "compra",
        "quantidade": 5,
        "preco_unitario": 30,
        "custo_total": 150
    }

    resp = client.post("/api/acoes/transacao", json=payload)
    assert resp.status_code == 201
    assert resp.get_json()["msg"] == "Operação registrada"


# ---------------------------------------------------------
# DELETE /api/acoes/<id_investimento>
# ---------------------------------------------------------
@patch("investment_data_service.controller_storage.api_controller.delete_investimento_api")
def test_deletar_invest_api(mock_delete, client):
    resp = client.delete("/api/acoes/1")
    assert resp.status_code == 200
    assert resp.get_json()["msg"] == "Investimento excluído com sucesso"

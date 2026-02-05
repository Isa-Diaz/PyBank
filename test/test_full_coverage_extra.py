
import pytest
from unittest.mock import patch, MagicMock
import sqlite3
from investment_data_service import app as app_module
import investment_data_service.repository.database as db


@pytest.fixture
def client():
    app = app_module.app
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ==========================================================
# COBRINDO app.py (linha do __main__)
# ==========================================================
def test_app_import_no_run():
    # Apenas testa se o app importa sem rodar o servidor
    assert hasattr(app_module, "app")


# ==========================================================
# COBERTURA FALTANTE – ADM CONTROLLER (25 LINHAS)
# ==========================================================

@patch("investment_data_service.controller_storage.adm_controller.buscar_investimento_por_id")
def test_buscar_investimento_por_id_404(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.get("/admin/investimento/id/999")
    assert resp.status_code == 404


@patch("investment_data_service.controller_storage.adm_controller.listar_user")
def test_listar_clientes_vazio(mock_list, client):
    mock_list.return_value = []
    resp = client.get("/admin/clientes")
    assert resp.status_code == 200
    assert resp.get_json() == []


@patch("investment_data_service.controller_storage.adm_controller.listar_investidores")
def test_listar_investidor_vazio(mock_list, client):
    mock_list.return_value = []
    resp = client.get("/admin/investidor")
    assert resp.status_code == 200
    assert resp.get_json() == []


@patch("investment_data_service.controller_storage.adm_controller.listar_investimentos")
def test_listar_investimentos_vazio(mock_list, client):
    mock_list.return_value = []
    resp = client.get("/admin/investimentos")
    assert resp.status_code == 200
    assert resp.get_json() == []


# ==========================================================
# COBERTURA EXTRA – CLIENTE CONTROLLER (1 LINHA)
# ==========================================================

@patch("investment_data_service.controller_storage.cliente_controller.insert_user")
def test_criar_cliente_telefone_lista(mock_insert, client):
    mock_insert.return_value = "123"
    resp = client.post("/clientes", json={
        "telefone": ["11900001111"],
        "cpf": "12345678901",
        "email": "x@x.com",
        "senha": "123"
    })
    assert resp.status_code == 201


# ==========================================================
# COBERTURA EXTRA – INVESTIMENT CONTROLLER (5 LINHAS)
# ==========================================================

@patch("investment_data_service.controller_storage.investiment_controller.listar_investimentos")
def test_listar_investimentos_cliente_vazio(mock_list, client):
    mock_list.return_value = [
        (1, "X", "CDB", 1, "2020", 1, 1)
    ]
    resp = client.get("/admin/investimentos/1")
    assert resp.status_code == 200
    assert resp.get_json() == []


# ==========================================================
# COBERTURA EXTRA – REPOSITORY (64 LINHAS)
# ==========================================================

def mock_conn():
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor
    return conn, cursor


# ---- INSERTS COM ERRO ----
@patch("sqlite3.connect")
def test_insert_tipo_investimento_integrity_error(mock_sql):
    conn, cursor = mock_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.IntegrityError()
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_tipo_investimento("1", "CDB", 1, "2020", 1, 1)


@patch("sqlite3.connect")
def test_insert_investimento_api_error(mock_sql):
    conn, cursor = mock_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.insert_investimento_api("1", "PETR4", 1, 10, 10)


@patch("sqlite3.connect")
def test_insert_transacao_error(mock_sql):
    conn, cursor = mock_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.insert_transacao("1", "deposito", 10, "X")


# ---- SELECTS RETORNANDO None OU LISTA VAZIA ----
@patch("sqlite3.connect")
def test_buscar_user_por_id_none(mock_sql):
    conn, cursor = mock_conn()
    mock_sql.return_value = conn
    cursor.fetchone.return_value = None
    result = db.buscar_user_por_id("1")
    assert result is None


@patch("sqlite3.connect")
def test_listar_user_vazio(mock_sql):
    conn, cursor = mock_conn()
    mock_sql.return_value = conn
    cursor.fetchall.return_value = []
    result = db.listar_user()
    assert result == []


@patch("sqlite3.connect")
def test_buscar_user_por_cpf_e_senha_none(mock_sql):
    conn, cursor = mock_conn()
    mock_sql.return_value = conn
    cursor.fetchone.return_value = None
    result = db.buscar_user_por_cpf_e_senha("123", "X")
    assert result is None


# ---- UPDATE SEM CAMPOS ----
def test_atualizar_user_sem_campos():
    result = db.atualizar_user("1")
    assert result == "Nenhum campo enviado para atualizar."


def test_atualizar_investidor_sem_campos():
    result = db.atualizar_investidor("1")
    assert "Nenhum campo" in result


def test_atualizar_investimento_sem_campos():
    result = db.atualizar_investimento("1")
    assert "Nenhum campo" in result


# ---- DELETE COM ERRO ----
@patch("sqlite3.connect")
def test_delete_user_operational_error(mock_sql):
    conn, cursor = mock_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.delete_user("1")


@patch("sqlite3.connect")
def test_delete_investimento_error(mock_sql):
    conn, cursor = mock_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.delete_investimento(1)


@patch("sqlite3.connect")
def test_delete_investimento_api_error(mock_sql):
    conn, cursor = mock_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.delete_investimento_api(1)

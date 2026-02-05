
import pytest
from unittest.mock import patch, MagicMock
import sqlite3

from investment_data_service.app import app as flask_app
import investment_data_service.repository.database as db


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ============================================================
# 1. COMPLEMENTO DO ADM_CONTROLLER (rotas e erros faltantes)
# ============================================================

@patch("investment_data_service.controller_storage.adm_controller.buscar_investimento_por_id")
def test_adm_buscar_investimento_id_ok(mock_buscar, client):
    mock_buscar.return_value = (1, "1", "CDB", 1000, "2024", 0.1, 1)
    resp = client.get("/admin/investimento/id/1")
    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.adm_controller.atualizar_investimento")
@patch("investment_data_service.controller_storage.adm_controller.buscar_investimento_por_id")
def test_adm_atualizar_investimento_body_incompleto(mock_buscar, mock_update, client):
    mock_buscar.return_value = (1,)
    resp = client.patch("/admin/investimentos/atualiza/1", json={})
    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.adm_controller.atualizar_investidor")
@patch("investment_data_service.controller_storage.adm_controller.buscar_investidor_por_id")
@patch("investment_data_service.controller_storage.adm_controller.buscar_user_por_id")
def test_adm_atualizar_investidor_none_fields(mock_user, mock_inv, mock_update, client):
    mock_user.return_value = ("1",)
    mock_inv.return_value = ("1",)
    resp = client.patch("/admin/investidor/id/atualiza/1", json={})
    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.adm_controller.buscar_investidor_por_id")
def test_adm_buscar_investidor_quando_none(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.get("/admin/investidor/id/1")
    assert resp.status_code == 404


# ============================================================
# 2. COMPLEMENTO DO INVESTIMENT_CONTROLLER (rotas faltantes)
# ============================================================

@patch("investment_data_service.controller_storage.investiment_controller.listar_investimentos")
def test_inv_listar_investimentos_cliente_vazio(mock_list, client):
    mock_list.return_value = []
    resp = client.get("/admin/investimentos/1")
    assert resp.status_code == 200
    assert resp.get_json() == []


@patch("investment_data_service.controller_storage.investiment_controller.buscar_investimento_por_id")
def test_inv_buscar_investimento_none(mock_buscar, client):
    mock_buscar.return_value = None
    resp = client.get("/admin/investimentos/1")
    assert resp.status_code == 200


@patch("investment_data_service.controller_storage.investiment_controller.atualizar_investimento")
@patch("investment_data_service.controller_storage.investiment_controller.buscar_investimento_por_id")
def test_inv_update_sem_novos_campos(mock_buscar, mock_update, client):
    mock_buscar.return_value = (1,)
    resp = client.patch("/admin/investimentos/1", json={})
    assert resp.status_code == 200

# ============================================================
# 3. TESTES COMPLEMENTARES DO DATABASE (61 linhas faltantes)
# ============================================================

def make_conn():
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor
    return conn, cursor


# ---------- INSERT ERROS ----------

@patch("sqlite3.connect")
def test_insert_user_error(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.insert_user("a","b","c","d",1,1,1,1,"x")


@patch("sqlite3.connect")
def test_insert_investidor_error(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.IntegrityError()
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_investidor("1","perfil",10,"2024")


@patch("sqlite3.connect")
def test_insert_investimentos_api_error(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.insert_investimento_api("1","PETR4",10,10,10)


@patch("sqlite3.connect")
def test_insert_transacao_error_internal(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.insert_transacao("1","deposito",10,"x")


# ---------- SELECT NONE ----------

@patch("sqlite3.connect")
def test_buscar_cpf_none(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.fetchone.return_value = None
    assert db.buscar_user_por_cpf("xxx") is None


@patch("sqlite3.connect")
def test_buscar_email_none(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.fetchone.return_value = None
    assert db.buscar_user_por_email("x@x") is None


@patch("sqlite3.connect")
def test_buscar_tel_none(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.fetchone.return_value = None
    assert db.buscar_user_por_telefone("999") is None


# ---------- SELECT EMPTY LIST ----------

@patch("sqlite3.connect")
def test_listar_inv_api_vazio(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.fetchall.return_value = []
    assert db.listar_investimentos_api("1") == []


@patch("sqlite3.connect")
def test_listar_transacoes_vazio(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.fetchall.return_value = []
    assert db.listar_transacoes("1") == []


# ---------- UPDATE ERROS ----------

@patch("sqlite3.connect")
def test_update_user_error(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.atualizar_user("1", nome="x")


@patch("sqlite3.connect")
def test_update_investidor_error(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.atualizar_investidor("1", perfil_investidor="x")


@patch("sqlite3.connect")
def test_update_investimento_error(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.atualizar_investimento("1", cliente_id="1")

# ---------- DELETE ERROS ----------

@patch("sqlite3.connect")
def test_delete_user_error(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.delete_user("1")


@patch("sqlite3.connect")
def test_delete_inv_error(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.delete_investimento(1)


@patch("sqlite3.connect")
def test_delete_inv_api_error(mock_sql):
    conn, cursor = make_conn()
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.delete_investimento_api(1)


# ---------- EXTRA BRANCHES ----------

def test_atualizar_user_sem_opcoes():
    assert db.atualizar_user("1") == "Nenhum campo enviado para atualizar."


def test_atualizar_investimento_sem_opcoes():
    assert db.atualizar_investimento("1") == "Nenhum campo enviado para atualizar."


# -------- registrar_operacao_api erro --------


@patch("sqlite3.connect")
def test_registrar_operacao_api_error(mock_sql):
    conn, cursor = make_conn()   # CERTO
    mock_sql.return_value = conn
    cursor.execute.side_effect = sqlite3.OperationalError()
    with pytest.raises(sqlite3.OperationalError):
        db.registrar_operacao_api("1", "PETR4", "compra", 10, 20, 200)

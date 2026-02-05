import pytest
from unittest.mock import patch, MagicMock

import investment_data_service.repository.database as db


# ---------------------------------------------------------
# Função auxiliar para mock de sqlite3
# ---------------------------------------------------------
def mock_conn_cursor():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


# ---------------------------------------------------------
# INSERT USER
# ---------------------------------------------------------
@patch("sqlite3.connect")
def test_insert_user(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.lastrowid = "uuid"
    result = db.insert_user("a","b","c","d",1,2,3,4,"senha")

    assert isinstance(result, str)


# ---------------------------------------------------------
# INSERT INVESTIDOR
# ---------------------------------------------------------
@patch("sqlite3.connect")
def test_insert_investidor(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    result = db.insert_investidor("1","moderado",1000,"2024-01-01")
    assert result == "1"


# ---------------------------------------------------------
# INSERT TIPO INVESTIMENTO
# ---------------------------------------------------------
@patch("sqlite3.connect")
def test_insert_tipo_investimento(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.lastrowid = 10
    result = db.insert_tipo_investimento("1","CDB",1000,"2024","0.1",1)

    assert result == (10, "1")


# ---------------------------------------------------------
# INSERT INVESTIMENTO API
# ---------------------------------------------------------
@patch("sqlite3.connect")
def test_insert_investimento_api(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.lastrowid = 5
    result = db.insert_investimento_api("1","PETR4",10,20,200)
    assert result == 5


# ---------------------------------------------------------
# INSERT TRANSACAO
# ---------------------------------------------------------
@patch("sqlite3.connect")
def test_insert_transacao(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.lastrowid = 33
    result = db.insert_transacao("1","deposito",100,"teste")
    assert result == 33


# ---------------------------------------------------------
# LISTAR FUNÇÕES
# ---------------------------------------------------------
@patch("sqlite3.connect")
def test_listar_user(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.fetchall.return_value = [("1","Joao")]
    result = db.listar_user()
    assert len(result) == 1


@patch("sqlite3.connect")
def test_listar_investidores(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.fetchall.return_value = [(1,"moderado")]
    result = db.listar_investidores()
    assert len(result) == 1


@patch("sqlite3.connect")
def test_listar_investimentos(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.fetchall.return_value = [(1,"1","CDB")]
    result = db.listar_investimentos()
    assert len(result) == 1


@patch("sqlite3.connect")
def test_listar_transacoes(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.fetchall.return_value = [(1,"1","deposito")]
    result = db.listar_transacoes("1")
    assert len(result) == 1


# ---------------------------------------------------------
# BUSCAR FUNÇÕES
# ---------------------------------------------------------
@patch("sqlite3.connect")
def test_buscar_user_por_id(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.fetchone.return_value = ("1","Joao")
    result = db.buscar_user_por_id("1")
    assert result[0] == "1"


@patch("sqlite3.connect")
def test_buscar_cliente_com_investidor(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.fetchone.return_value = ("1","Joao")
    result = db.buscar_cliente_com_investidor("1")
    assert result is not None


@patch("sqlite3.connect")
def test_buscar_investidor_por_id(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.fetchone.return_value = ("1","moderado")
    result = db.buscar_investidor_por_id("1")
    assert result is not None


@patch("sqlite3.connect")
def test_buscar_investimento_por_id(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.fetchone.return_value = (1,"1","CDB")
    result = db.buscar_investimento_por_id("1")
    assert result is not None


# ---------------------------------------------------------
# UPDATE FUNÇÕES
# ---------------------------------------------------------
@patch("sqlite3.connect")
def test_atualizar_user(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    result = db.atualizar_user("1", nome="Joao")
    assert "sucesso" in result.lower()


@patch("sqlite3.connect")
def test_atualizar_investidor(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    result = db.atualizar_investidor("1", perfil_investidor="moderado")
    assert "sucesso" in result.lower()


@patch("sqlite3.connect")
def test_atualizar_investimento(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    result = db.atualizar_investimento("1", cliente_id="1")
    assert "sucesso" in result.lower()


@patch("sqlite3.connect")
def test_atualizar_investimento_api(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    db.atualizar_investimento_api(1,10,200)
    cursor.execute.assert_called()


# ---------------------------------------------------------
# DELETE FUNÇÕES
# ---------------------------------------------------------
@patch("sqlite3.connect")
def test_delete_user(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    db.delete_user("1")
    cursor.execute.assert_called()


@patch("sqlite3.connect")
def test_delete_investimento(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    db.delete_investimento(1)
    cursor.execute.assert_called()


@patch("sqlite3.connect")
def test_delete_investimento_api(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    db.delete_investimento_api(1)
    cursor.execute.assert_called()


# ---------------------------------------------------------
# LOGIN E SENHA
# ---------------------------------------------------------
@patch("sqlite3.connect")
def test_buscar_user_por_cpf_e_senha(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    cursor.fetchone.return_value = ("1","Joao")
    result = db.buscar_user_por_cpf_e_senha("123","senha")
    assert result is not None


@patch("sqlite3.connect")
def test_atualizar_senha_por_id(mock_sql):
    conn, cursor = mock_conn_cursor()
    mock_sql.return_value = conn

    db.atualizar_senha_por_id("1","abc")
    cursor.execute.assert_called()

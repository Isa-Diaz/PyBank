import pytest
from unittest.mock import MagicMock, patch
import client_access_service.client.client_access as client


# ============================================================
# buscar_cliente_por_cpf
# ============================================================

@patch("client_access_service.client.client_access.requests.get")
def test_buscar_cliente_por_cpf_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    resp = client.buscar_cliente_por_cpf("12345678901")
    assert resp.status_code == 200


@patch("client_access_service.client.client_access.requests.get")
def test_buscar_cliente_por_cpf_erro(mock_get):
    mock_get.return_value = MagicMock(status_code=500)
    resp = client.buscar_cliente_por_cpf("12345678901")
    assert resp.status_code == 500

# ============================================================
# criar_cliente
# ============================================================

@patch("client_access_service.client.client_access.requests.post")
def test_criar_cliente_ok(mock_post):
    mock_post.return_value = MagicMock(status_code=201)
    resp = client.criar_cliente({"nome": "Joao"})
    assert resp.status_code == 201


@patch("client_access_service.client.client_access.requests.post")
def test_criar_cliente_erro(mock_post):
    mock_post.return_value = MagicMock(status_code=500)
    resp = client.criar_cliente({"nome": "Joao"})
    assert resp.status_code == 500


# ============================================================
# atualizar_cliente_por_cpf
# ============================================================

@patch("client_access_service.client.client_access.requests.patch")
def test_atualizar_cliente_por_cpf_ok(mock_patch):
    mock_patch.return_value = MagicMock(status_code=200)
    resp = client.atualizar_cliente_por_cpf("123", {"nome": "Novo"})
    assert resp.status_code == 200


@patch("client_access_service.client.client_access.requests.patch")
def test_atualizar_cliente_por_cpf_erro(mock_patch):
    mock_patch.return_value = MagicMock(status_code=500)
    resp = client.atualizar_cliente_por_cpf("123", {"nome": "Novo"})
    assert resp.status_code == 500

# ============================================================
# buscar_user_por_email
# ============================================================

@patch("client_access_service.client.client_access.requests.get")
def test_buscar_user_por_email_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    resp = client.buscar_user_por_email("a@a.com")
    assert resp.status_code == 200


@patch("client_access_service.client.client_access.requests.get")
def test_buscar_user_por_email_erro(mock_get):
    mock_get.return_value = MagicMock(status_code=500)
    resp = client.buscar_user_por_email("a@a.com")
    assert resp.status_code == 500


# ============================================================
# buscar_user_telefone
# ============================================================

@patch("client_access_service.client.client_access.requests.get")
def test_buscar_user_telefone_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    resp = client.buscar_user_telefone("11999999999")
    assert resp.status_code == 200


@patch("client_access_service.client.client_access.requests.get")
def test_buscar_user_telefone_erro(mock_get):
    mock_get.return_value = MagicMock(status_code=500)
    resp = client.buscar_user_telefone("11999999999")
    assert resp.status_code == 500


# ============================================================
# criar_transacao
# ============================================================

@patch("client_access_service.client.client_access.requests.post")
def test_criar_transacao_ok(mock_post):
    mock_post.return_value = MagicMock(status_code=201)
    resp = client.criar_transacao({"valor": 50})
    assert resp.status_code == 201


@patch("client_access_service.client.client_access.requests.post")
def test_criar_transacao_erro(mock_post):
    mock_post.return_value = MagicMock(status_code=500)
    resp = client.criar_transacao({"valor": 50})
    assert resp.status_code == 500


# ============================================================
# login_ms1
# ============================================================

@patch("client_access_service.client.client_access.requests.post")
def test_login_ms1_ok(mock_post):
    mock_post.return_value = MagicMock(status_code=200)
    resp = client.login_ms1("123", "abc")
    assert resp.status_code == 200


@patch("client_access_service.client.client_access.requests.post")
def test_login_ms1_erro(mock_post):
    mock_post.return_value = MagicMock(status_code=500)
    resp = client.login_ms1("123", "abc")
    assert resp.status_code == 500


# ============================================================
# alterar_senha_ms1
# ============================================================

@patch("client_access_service.client.client_access.requests.patch")
def test_alterar_senha_ms1_ok(mock_patch):
    mock_patch.return_value = MagicMock(status_code=200)
    resp = client.alterar_senha_ms1("123", "old", "new")
    assert resp.status_code == 200


@patch("client_access_service.client.client_access.requests.patch")
def test_alterar_senha_ms1_erro(mock_patch):
    mock_patch.return_value = MagicMock(status_code=500)
    resp = client.alterar_senha_ms1("123", "old", "new")
    assert resp.status_code == 500

import pytest
from unittest.mock import MagicMock, patch

import client_access_service.service.cliente_service_access as service


# ============================================================
# TESTANDO processar_dados
# ============================================================

def test_processar_dados_nome_vazio():
    resp = service.processar_dados({"nome": "", "cpf": "123", "email": "a", "telefone": "1", "senha": "1"})
    assert resp["valido"] == False


def test_processar_dados_cpf_invalido():
    resp = service.processar_dados({"nome": "Joao", "cpf": "ABC", "email": "a", "telefone": "1", "senha": "1"})
    assert resp["valido"] == False


@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_processar_dados_cpf_existente(mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {}, status_code=200)
    resp = service.processar_dados({
        "nome": "Joao",
        "cpf": "12345678901",
        "email": "a@a.com",
        "telefone": "11999999999",
        "senha": "123"
    })
    assert resp["valido"] == False


@patch("client_access_service.service.cliente_service_access.buscar_user_por_email")
def test_processar_dados_email_ja_existe(mock_email):
    mock_email.return_value = MagicMock(json=lambda: {}, status_code=200)
    resp = service.processar_dados({
        "nome": "Joao",
        "cpf": "12345678901",
        "email": "x@x.com",
        "telefone": "11999999999",
        "senha": "123"
    })
    assert resp["valido"] == False


@patch("client_access_service.service.cliente_service_access.buscar_user_telefone")
def test_processar_dados_telefone_existente(mock_tel):
    mock_tel.return_value = MagicMock(json=lambda: {}, status_code=200)
    resp = service.processar_dados({
        "nome": "Joao",
        "cpf": "12345678901",
        "email": "x@x.com",
        "telefone": "11999999999",
        "senha": "123"
    })
    assert resp["valido"] == False


def test_processar_dados_sucesso():
    ok = service.processar_dados({
        "nome": "Joao",
        "cpf": "12345678901",
        "email": "a@a.com",
        "telefone": "11999999999",
        "senha": "abc"
    })
    assert ok["valido"] == True


# ============================================================
# TESTANDO processar_correntista
# ============================================================

def test_processar_correntista_saldo_negativo():
    resp = service.processar_correntista({"correntista": True, "saldo_cc": -10})
    assert "erro" in resp


def test_processar_correntista_nao_correntista_com_saldo():
    resp = service.processar_correntista({"correntista": False, "saldo_cc": 100})
    assert "erro" in resp


def test_processar_correntista_valor_invalido_string():
    resp = service.processar_correntista({"correntista": True, "saldo_cc": "abc"})
    assert "erro" in resp


def test_processar_correntista_ok():
    resp = service.processar_correntista({"correntista": True, "saldo_cc": 100})
    assert resp["score_credito"] > 0


# ============================================================
# criar_cliente_service
# ============================================================

@patch("client_access_service.service.cliente_service_access.criar_cliente")
def test_criar_cliente_service_sucesso(mock_create):
    mock_create.return_value = MagicMock(json=lambda: {"id": "1"}, status_code=200)

    dados = {
        "nome": "Joao",
        "cpf": "12345678901",
        "email": "a@a.com",
        "telefone": "11999999999",
        "senha": "123",
        "correntista": True,
        "saldo_cc": 0
    }

    resp, status = service.criar_cliente_service(dados)
    assert status == 200


def test_criar_cliente_service_validacao_falha():
    resp, status = service.criar_cliente_service({"nome": ""})
    assert status == 400


# ============================================================
# atualizar_cliente_service
# ============================================================

@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_atualizar_cliente_service_nao_encontrado(mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {}, status_code=404)
    resp, status = service.atualizar_cliente_service("123", {})
    assert status == 404


@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.atualizar_cliente_por_cpf")
def test_atualizar_cliente_service_ok(mock_update, mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {"email": "x@x.com", "telefone": "1199"}, status_code=200)
    mock_update.return_value = MagicMock(json=lambda: {"msg": "ok"}, status_code=200)

    resp, status = service.atualizar_cliente_service("123", {"nome": "novo"})
    assert status == 200


# ============================================================
# operacao_service
# ============================================================

def test_operacao_service_validacao_tipo_invalido():
    resp, status = service.operacao_service("123", {"tipo": "ERRADO", "valor": 10})
    assert status == 400


@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_operacao_service_cliente_nao_encontrado(mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {}, status_code=404)
    resp, status = service.operacao_service("123", {"tipo": "deposito", "valor": 10})
    assert status == 404


@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_operacao_service_nao_correntista(mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {"correntista": 0}, status_code=200)
    resp, status = service.operacao_service("123", {"tipo": "deposito", "valor": 10})
    assert status == 400


@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_operacao_service_saque_saldo_insuficiente(mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {"correntista": 1, "saldo_cc": 5}, status_code=200)
    resp, status = service.operacao_service("123", {"tipo": "saque", "valor": 10})
    assert status == 400


@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.atualizar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.criar_transacao")
def test_operacao_service_ok(mock_trans, mock_update, mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {"correntista": 1, "saldo_cc": 100, "id": "1"}, status_code=200)
    mock_update.return_value = MagicMock(json=lambda: {"msg": "ok"}, status_code=200)

    resp, status = service.operacao_service("123", {"tipo": "deposito", "valor": 50})
    assert status == 200


# ============================================================
# listar_transacoes_cpf
# ============================================================

@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.listar_transacoes_por_id")
def test_listar_transacoes_cpf_ok(mock_listar, mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {"id": "1"}, status_code=200)
    mock_listar.return_value = [{"id": 1}]
    resp = service.listar_transacoes_cpf("123")
    assert isinstance(resp, list)


# ============================================================
# login_service
# ============================================================

@patch("client_access_service.service.cliente_service_access.login_ms1")
def test_login_service_ok(mock_login):
    mock_login.return_value = MagicMock(json=lambda: {"id": 1}, status_code=200)
    resp, status = service.login_service("123", "abc")
    assert status == 200


@patch("client_access_service.service.cliente_service_access.login_ms1")
def test_login_service_senha_errada(mock_login):
    mock_login.return_value = MagicMock(json=lambda: {}, status_code=401)
    resp, status = service.login_service("123", "abc")
    assert status == 401



@patch("client_access_service.service.cliente_service_access.login_ms1")
def test_login_service_nao_encontrado(mock_login):
    mock_login.return_value = MagicMock(json=lambda: {}, status_code=404)
    resp, status = service.login_service("123", "abc")
    assert status == 404


# ============================================================
# alterar_senha_service
# ============================================================

@patch("client_access_service.service.cliente_service_access.alterar_senha_ms1")
def test_alterar_senha_service_ok(mock_patch):
    mock_patch.return_value = MagicMock(json=lambda: {"msg": "ok"}, status_code=200)
    resp, status = service.alterar_senha_service("123", "old", "new")
    assert status == 200


# ============================================================
# buscar_cliente_service
# ============================================================

@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_buscar_cliente_service_ok(mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {"id": 1}, status_code=200)
    resp, status = service.buscar_cliente_service("123")
    assert status == 200


@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_buscar_cliente_service_nao_encontrado(mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {}, status_code=404)
    resp, status = service.buscar_cliente_service("123")
    assert status == 404


# ============================================================
# deletar_cliente_service
# ============================================================

@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_deletar_cliente_service_cliente_nao_existe(mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {}, status_code=404)
    resp, status = service.deletar_cliente_service("123")
    assert status == 404


@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_deletar_cliente_service_saldo_nao_zero(mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {"id": 1, "saldo_cc": 50, "admin": 0}, status_code=200)
    resp, status = service.deletar_cliente_service("123")
    assert status == 400


@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_deletar_cliente_service_admin_nao_pode_se_apagar(mock_buscar):
    mock_buscar.return_value = MagicMock(json=lambda: {"id": 1, "saldo_cc": 0, "admin": 1}, status_code=200)
    resp, status = service.deletar_cliente_service("123")
    assert status == 403



@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
@patch("client_access_service.client.adm_access.deletar_cliente_por_id")
def test_deletar_cliente_service_ok(mock_delete, mock_buscar):
    mock_buscar.return_value = MagicMock(
        json=lambda: {"id": 1, "saldo_cc": 0, "admin": 0},
        status_code=200
    )
    mock_delete.return_value = MagicMock(
        json=lambda: {"msg": "apagado"},
        status_code=200
    )

    resp, status = service.deletar_cliente_service("123")
    assert status == 200

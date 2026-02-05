# test/test_cliente_service_access_coverage_extra.py

import pytest
from unittest.mock import MagicMock, patch

import client_access_service.service.cliente_service_access as svc


# ---------------- ler_resposta ----------------

def test_ler_resposta_none():
    resp, status = svc.ler_resposta(None)
    assert status == 500
    assert resp["erro"] == "MS1 fora do ar"


def test_ler_resposta_json_invalido():
    fake = MagicMock(status_code=200)
    fake.json.side_effect = Exception("err")
    fake.text = "texto erro"
    resp, status = svc.ler_resposta(fake)
    assert resp == {"erro": "texto erro"}
    assert status == 200


# ---------------- processar_dados ----------------

@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.buscar_user_por_email")
@patch("client_access_service.service.cliente_service_access.buscar_user_telefone")
def test_processar_dados_sucesso_branches(mock_tel, mock_email, mock_cpf):
    mock_cpf.return_value = MagicMock(status_code=404, json=lambda: {})
    mock_email.return_value = MagicMock(status_code=404, json=lambda: {})
    mock_tel.return_value = MagicMock(status_code=404, json=lambda: {})

    dados = {
        "nome": " Ana  ",
        "cpf": "12345678901",
        "email": "a@a.com",
        "telefone": "11999999999",
        "senha": "abc",
        "admin": 0
    }

    resp = svc.processar_dados(dados)
    assert resp["valido"] is True
    assert resp["dados"]["nome"] == "Ana"
# test/test_cliente_service_access_update_extra.py

import pytest
from unittest.mock import MagicMock, patch

import client_access_service.service.cliente_service_access as svc


def mock_resp(json_data, status):
    return MagicMock(json=lambda: json_data, status_code=status)


# ---------------- email duplicado ----------------

@patch("client_access_service.service.cliente_service_access.buscar_user_por_email")
@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_atualizar_cliente_email_duplicado(mock_cpf, mock_email):
    mock_cpf.return_value = mock_resp({"email": "old@mail.com"}, 200)
    mock_email.return_value = mock_resp({}, 200)
    resp, status = svc.atualizar_cliente_service("1", {"email": "new@mail.com"})
    assert status == 400
    assert resp["erro"] == "Email já cadastrado"


# ---------------- telefone duplicado ----------------

@patch("client_access_service.service.cliente_service_access.buscar_user_telefone")
@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_atualizar_cliente_telefone_duplicado(mock_cpf, mock_tel):
    mock_cpf.return_value = mock_resp({"telefone": "111"}, 200)
    mock_tel.return_value = mock_resp({}, 200)
    resp, status = svc.atualizar_cliente_service("1", {"telefone": "222"})
    assert status == 400
    assert resp["erro"] == "Telefone já cadastrado"


# ---------------- update no MS1 deu erro ----------------

@patch("client_access_service.service.cliente_service_access.atualizar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_atualizar_cliente_update_falhou(mock_cpf, mock_update):
    mock_cpf.return_value = mock_resp({"email": "x", "telefone": "1"}, 200)
    mock_update.return_value = mock_resp({"erro": "x"}, 500)

    resp, status = svc.atualizar_cliente_service("1", {"nome": "novo"})
    assert status == 500
    assert resp["erro"] == "Falha ao atualizar no MS1"


# ---------------- update OK (branch final) ----------------

@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.atualizar_cliente_por_cpf")
def test_atualizar_cliente_sucesso(mock_update, mock_cpf):

    mock_cpf.side_effect = [
        mock_resp({"email": "x", "telefone": "1"}, 200),   # antes update
        mock_resp({"nome": "novo"}, 200)                   # depois update
    ]
    mock_update.return_value = mock_resp({}, 200)

    resp, status = svc.atualizar_cliente_service("1", {"nome": "novo"})
    assert status == 200
    assert resp["msg"] == "Cliente atualizado com sucesso"

# test/test_cliente_service_access_final_extra.py

import pytest
from unittest.mock import MagicMock, patch
import client_access_service.service.cliente_service_access as svc


def mock_resp(json_data, status):
    return MagicMock(json=lambda: json_data, status_code=status)


# ============================================================
# operacao_service — update de saldo falhou
# (cobre linhas 188 e 206)
# ============================================================

@patch("client_access_service.service.cliente_service_access.atualizar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_operacao_service_update_falha(mock_cpf, mock_update):
    mock_cpf.return_value = mock_resp(
        {"id": 1, "correntista": 1, "saldo_cc": 5},
        200
    )
    mock_update.return_value = mock_resp({"erro": "x"}, 500)

    resp, status = svc.operacao_service("123", {"tipo": "deposito", "valor": 10})
    assert status == 500
    assert resp["erro"] == "Falha ao atualizar saldo no MS1"

# ============================================================
# listar_transacoes_cpf — cliente não encontrado
# (cobre linha 206)
# ============================================================

@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_listar_transacoes_cpf_cliente_404(mock_cpf):
    mock_cpf.return_value = mock_resp({}, 404)

    resp = svc.listar_transacoes_cpf("999")
    assert resp == ({"erro": "Cliente não encontrado"}, 404)

# ============================================================
# deletar_cliente_service — branch final (sucesso)
# cobre linha 222
# ============================================================

@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
@patch("client_access_service.client.adm_access.deletar_cliente_por_id")
def test_deletar_cliente_service_final(mock_del, mock_cpf):
    mock_cpf.return_value = mock_resp(
        {"id": 1, "saldo_cc": 0, "admin": 0},
        200
    )
    mock_del.return_value = mock_resp({"msg": "apagado"}, 200)

    resp, status = svc.deletar_cliente_service("123")
    assert status == 200
    assert resp["msg"] == "apagado"

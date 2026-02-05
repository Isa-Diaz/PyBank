
# test/test_cliente_service_access_full_coverage.py

import pytest
from unittest.mock import MagicMock, patch
import client_access_service.service.cliente_service_access as svc


def mock_resp(json_data, status):
    return MagicMock(json=lambda: json_data, status_code=status)


# ============================================================
# 1) ler_resposta – cobrir resp=None e json inválido
# ============================================================

def test_ler_resposta_none():
    body, status = svc.ler_resposta(None)
    assert status == 500
    assert body["erro"] == "MS1 fora do ar"


def test_ler_resposta_json_invalido():
    fake = MagicMock(status_code=200)
    fake.json.side_effect = Exception("bad json")
    fake.text = "erro bruto"
    body, status = svc.ler_resposta(fake)
    assert status == 200
    assert body["erro"] == "erro bruto"


# ============================================================
# 2) processar_dados – cobrir senha obrigatória (linha 52)
# ============================================================

def test_processar_dados_senha_obrigatoria():
    resp = svc.processar_dados({
        "nome": "Ana",
        "cpf": "12345678901",
        "email": "x@x.com",
        "telefone": "11999999999",
        "senha": ""
    })
    assert resp["valido"] is False
    assert "Senha é obrigatória" in resp["erro"]

# ============================================================
# 3) processar_dados – cobrir retorno final completo (linha 60)
# ============================================================

@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.buscar_user_por_email")
@patch("client_access_service.service.cliente_service_access.buscar_user_telefone")
def test_processar_dados_sucesso_branches(mock_tel, mock_email, mock_cpf):
    mock_cpf.return_value = mock_resp({}, 404)
    mock_email.return_value = mock_resp({}, 404)
    mock_tel.return_value = mock_resp({}, 404)

    dados = {
        "nome": "Ana",
        "cpf": "12345678901",
        "email": "ana@ana.com",
        "telefone": "11999999999",
        "senha": "123",
        "admin": 1
    }

    resp = svc.processar_dados(dados)
    assert resp["valido"] is True
    assert resp["dados"]["admin"] == 1


# ============================================================
# 4) atualizar_cliente_service – email duplicado (linha 112)
# ============================================================

@patch("client_access_service.service.cliente_service_access.buscar_user_por_email")
@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.atualizar_cliente_por_cpf")
def test_atualizar_cliente_email_mesmo(mock_update, mock_cpf, mock_email):
    mock_cpf.return_value = mock_resp({"email": "a@a.com", "telefone": "1"}, 200)
    mock_email.return_value = mock_resp({}, 200)
    mock_update.return_value = mock_resp({}, 200)

    resp, status = svc.atualizar_cliente_service("1", {"email": "a@a.com"})
    assert status == 200


# ============================================================
# 5) atualizar_cliente_service – telefone duplicado (linha 129)
# ============================================================

@patch("client_access_service.service.cliente_service_access.buscar_user_telefone")
@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.atualizar_cliente_por_cpf")
def test_atualizar_cliente_telefone_mesmo(mock_update, mock_cpf, mock_tel):
    mock_cpf.return_value = mock_resp({"telefone": "123", "email": "a"}, 200)
    mock_tel.return_value = mock_resp({}, 200)
    mock_update.return_value = mock_resp({}, 200)

    resp, status = svc.atualizar_cliente_service("1", {"telefone": "123"})
    assert status == 200

# ============================================================
# 6) operacao_service – update de saldo falhou (linha 188)
# ============================================================

@patch("client_access_service.service.cliente_service_access.atualizar_cliente_por_cpf")
@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_operacao_service_update_falha(mock_cpf, mock_update):
    mock_cpf.return_value = mock_resp(
        {"id": 1, "correntista": 1, "saldo_cc": 5},
        200
    )
    mock_update.return_value = mock_resp({"erro": "falha"}, 500)

    resp, status = svc.operacao_service("100", {"tipo": "deposito", "valor": 10})
    assert status == 500
    assert resp["erro"] == "Falha ao atualizar saldo no MS1"


# ============================================================
# 7) listar_transacoes_cpf – cliente 404 (linha 206)
# ============================================================

@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
def test_listar_transacoes_cpf_cliente_404(mock_cpf):
    mock_cpf.return_value = mock_resp({}, 404)
    resp = svc.listar_transacoes_cpf("999")
    assert resp == ({"erro": "Cliente não encontrado"}, 404)


# ============================================================
# 8) deletar_cliente_service – MS1 fora do ar (linha 222)
# ============================================================

@patch("client_access_service.service.cliente_service_access.buscar_cliente_por_cpf")
@patch("client_access_service.client.adm_access.deletar_cliente_por_id")
def test_deletar_cliente_service_ms1_fora_do_ar(mock_del, mock_cpf):
    mock_cpf.return_value = mock_resp({"id": 1, "saldo_cc": 0, "admin": 0}, 200)
    mock_del.return_value = None  # simula MS1 fora

    resp, status = svc.deletar_cliente_service("123")
    assert status == 500
    assert resp["erro"] == "MS1 fora do ar"

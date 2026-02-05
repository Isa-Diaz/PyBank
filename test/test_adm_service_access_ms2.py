
import pytest
from unittest.mock import patch, MagicMock
from requests import RequestException

import client_access_service.client.adm_access as adm


# ============================================================
# listar_clientes
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_listar_clientes_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    resp = adm.listar_clientes()
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_listar_clientes_erro(mock_get):
    mock_get.side_effect = RequestException("erro")
    with pytest.raises(RequestException):
        adm.listar_clientes()

# ============================================================
# buscar_cliente_por_id
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_cliente_por_id_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    resp = adm.buscar_cliente_por_id("1")
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_cliente_por_id_erro(mock_get):
    mock_get.side_effect = RequestException("erro")
    with pytest.raises(RequestException):
        adm.buscar_cliente_por_id("1")


# ============================================================
# atualizar_cliente
# ============================================================

@patch("client_access_service.client.adm_access.requests.patch")
def test_atualizar_cliente_ok(mock_patch):
    mock_patch.return_value = MagicMock(status_code=200)
    resp = adm.atualizar_cliente("1", {"nome": "novo"})
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.patch")
def test_atualizar_cliente_erro(mock_patch):
    mock_patch.side_effect = RequestException("erro")
    with pytest.raises(RequestException):
        adm.atualizar_cliente("1", {"nome": "novo"})


# ============================================================
# listar_investidores
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_listar_investidores_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    resp = adm.listar_investidores()
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_listar_investidores_erro(mock_get):
    mock_get.side_effect = RequestException("erro")
    with pytest.raises(RequestException):
        adm.listar_investidores()

# ============================================================
# buscar_investidor_por_id
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_investidor_por_id_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    resp = adm.buscar_investidor_por_id("1")
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_investidor_por_id_erro(mock_get):
    mock_get.side_effect = RequestException("erro")
    with pytest.raises(RequestException):
        adm.buscar_investidor_por_id("1")


# ============================================================
# buscar_investidor_com_cliente
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_investidor_com_cliente_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    resp = adm.buscar_investidor_com_cliente("1")
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_investidor_com_cliente_erro(mock_get):
    mock_get.side_effect = RequestException("erro")
    with pytest.raises(RequestException):
        adm.buscar_investidor_com_cliente("1")


# ============================================================
# listar_transacoes_por_id
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_listar_transacoes_por_id_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    resp = adm.listar_transacoes_por_id("1")
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_listar_transacoes_por_id_erro(mock_get):
    mock_get.side_effect = RequestException("erro")
    with pytest.raises(RequestException):
        adm.listar_transacoes_por_id("1")


# ============================================================
# deletar_cliente_por_id
# ============================================================

@patch("client_access_service.client.adm_access.requests.delete")
def test_deletar_cliente_por_id_ok(mock_delete):
    mock_delete.return_value = MagicMock(status_code=200)
    resp = adm.deletar_cliente_por_id("1")
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.delete")
def test_deletar_cliente_por_id_erro(mock_delete):
    mock_delete.side_effect = RequestException("erro")
    resp = adm.deletar_cliente_por_id("1")
    assert resp is None

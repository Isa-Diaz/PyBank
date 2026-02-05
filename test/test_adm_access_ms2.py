import pytest
from unittest.mock import patch, MagicMock

import client_access_service.client.adm_access as adm


# ============================================================
# listar_clientes
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_listar_clientes_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {})
    resp = adm.listar_clientes()
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_listar_clientes_erro(mock_get):
    mock_get.return_value = MagicMock(status_code=500, json=lambda: {})
    resp = adm.listar_clientes()
    assert resp is None or resp == {}
    

# ============================================================
# buscar_cliente_por_id
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_cliente_por_id_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {})
    resp = adm.buscar_cliente_por_id("1")
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_cliente_por_id_erro(mock_get):
    mock_get.return_value = MagicMock(status_code=500, json=lambda: {})
    resp = adm.buscar_cliente_por_id("1")
    assert resp is None or resp == {}

# ============================================================
# atualizar_cliente
# ============================================================

@patch("client_access_service.client.adm_access.requests.patch")
def test_atualizar_cliente_ok(mock_patch):
    mock_patch.return_value = MagicMock(status_code=200, json=lambda: {})
    resp = adm.atualizar_cliente("1", {"nome": "novo"})
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.patch")
def test_atualizar_cliente_erro(mock_patch):
    mock_patch.return_value = MagicMock(status_code=500, json=lambda: {})
    resp = adm.atualizar_cliente("1", {"nome": "novo"})
    assert resp is None or resp == {}


# ============================================================
# listar_investidores
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_listar_investidores_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {})
    resp = adm.listar_investidores()
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_listar_investidores_erro(mock_get):
    mock_get.return_value = MagicMock(status_code=500, json=lambda: {})
    resp = adm.listar_investidores()
    assert resp is None or resp == {}


# ============================================================
# buscar_investidor_por_id
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_investidor_por_id_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {})
    resp = adm.buscar_investidor_por_id("1")
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_investidor_por_id_erro(mock_get):
    mock_get.return_value = MagicMock(status_code=500, json=lambda: {})
    resp = adm.buscar_investidor_por_id("1")
    assert resp is None or resp == {}


# ============================================================
# buscar_investidor_com_cliente
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_investidor_com_cliente_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {})
    resp = adm.buscar_investidor_com_cliente("1")
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_buscar_investidor_com_cliente_erro(mock_get):
    mock_get.return_value = MagicMock(status_code=500, json=lambda: {})
    resp = adm.buscar_investidor_com_cliente("1")
    assert resp is None or resp == {}


# ============================================================
# listar_transacoes_por_id
# ============================================================

@patch("client_access_service.client.adm_access.requests.get")
def test_listar_transacoes_por_id_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {})
    resp = adm.listar_transacoes_por_id("1")
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.get")
def test_listar_transacoes_por_id_erro(mock_get):
    mock_get.return_value = MagicMock(status_code=500, json=lambda: {})
    resp = adm.listar_transacoes_por_id("1")
    assert resp is None or resp == {}


# ============================================================
# deletar_cliente_por_id
# ============================================================

@patch("client_access_service.client.adm_access.requests.delete")
def test_deletar_cliente_por_id_ok(mock_delete):
    mock_delete.return_value = MagicMock(status_code=200, json=lambda: {})
    resp = adm.deletar_cliente_por_id("1")
    assert resp is not None


@patch("client_access_service.client.adm_access.requests.delete")
def test_deletar_cliente_por_id_erro(mock_delete):
    mock_delete.return_value = MagicMock(status_code=500, json=lambda: {})
    resp = adm.deletar_cliente_por_id("1")
    assert resp.status_code == 500

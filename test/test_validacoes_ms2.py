import pytest
from client_access_service.service.cliente_service_access import (
    validar_operacao,
    calcular_score,
    processar_dados,
    processar_correntista
)


# ============================================================
# validar_operacao
# ============================================================

def test_validar_operacao_tipo_invalido():
    assert validar_operacao({"tipo": "x", "valor": 10}) == "Tipo inválido"


def test_validar_operacao_valor_negativo():
    assert validar_operacao({"tipo": "saque", "valor": -1}) == "Valor deve ser maior que zero"


def test_validar_operacao_valor_invalido():
    assert validar_operacao({"tipo": "saque", "valor": "abc"}) == "Valor inválido"


def test_validar_operacao_ok():
    assert validar_operacao({"tipo": "deposito", "valor": 10}) is None


# ============================================================
# calcular_score
# ============================================================

def test_calcular_score_positivo():
    assert calcular_score(100) == 10


def test_calcular_score_zero():
    assert calcular_score(0) == 0


def test_calcular_score_negativo():
    assert calcular_score(-10) == 0


# ============================================================
# processar_dados (COBRIR CENÁRIOS RESTANTES)
# ============================================================

def test_processar_dados_campos_faltando():
    resp = processar_dados({})
    assert resp["valido"] is False


def test_processar_dados_senha_vazia():
    resp = processar_dados({"nome": "A", "cpf": "12345678901", "email": "x@x", "telefone": "11999999999", "senha": ""})
    assert resp["valido"] is False


# ============================================================
# processar_correntista (cobrir ramos faltantes)
# ============================================================

def test_processar_correntista_valor_invalido_tipo_string():
    resp = processar_correntista({"correntista": True, "saldo_cc": "abc"})
    assert "erro" in resp


def test_processar_correntista_false_saldo_zero_ok():
    resp = processar_correntista({"correntista": False, "saldo_cc": 0})
    assert resp["correntista"] == 0
    assert resp["saldo_cc"] == 0

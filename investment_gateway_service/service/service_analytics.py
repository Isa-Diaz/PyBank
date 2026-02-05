import pandas as pd
import numpy as np
from datetime import datetime

from ..client.client_invest import (
    buscar_cliente_por_cpf_ms1,
    listar_investimentos_cliente_ms1,
    buscar_investidor_ms1
)

from ..client.client_api import (
    buscar_investimento_api_ms1,
    listar_investimentos_api_ms1,
    buscar_cotacao_atual,
    buscar_historico_12m
)


# =====================================================
# HELPER: calcula retorno acumulado de uma série
# =====================================================
def retorno_acumulado(precos):
    preco_inicial = precos[0]
    preco_final = precos[-1]
    return round((preco_final - preco_inicial) / preco_inicial * 100, 2)


# =====================================================
# HELPER: calcula retorno anualizado
# Formula: (final/inicial)^(1/anos) - 1
# =====================================================
def retorno_anualizado(precos):
    preco_inicial = precos[0]
    preco_final = precos[-1]
    anos = 1  
    return round(((preco_final / preco_inicial) ** (1/anos) - 1) * 100, 2)


# =====================================================
# HELPER: volatilidade (desvio padrão dos retornos diários)
# =====================================================
def volatilidade(precos):
    serie = pd.Series(precos)
    retornos = serie.pct_change().dropna()
    vol = np.std(retornos) * np.sqrt(252) * 100  
    return round(vol, 2)



# =====================================================
# ANALISAR PERFORMANCE COMPLETA DA CARTEIRA
# =====================================================
def performance_carteira_service(cpf):

    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return cliente
    
    id_cliente = cliente["id"]

    investidor = buscar_investidor_ms1(id_cliente)
    if "erro" in investidor:
        return investidor
    
    patrimonio_total = float(investidor["patrimonio_total"])

    # -----------------------
    # Renda fixa
    # -----------------------
    investimentos_fixos = listar_investimentos_cliente_ms1(id_cliente)
    total_fixo = sum(inv["valor_investido"] for inv in investimentos_fixos)

    # -----------------------
    # Ações - renda variável
    # -----------------------
    investimentos_acoes = listar_investimentos_api_ms1(id_cliente)

    total_atual_acoes = 0
    total_investido_acoes = 0
    detalhes_acoes = []

    for acao in investimentos_acoes:
        preco_atual = buscar_cotacao_atual(acao["ticker"])["preco_atual"]
        valor_atual = preco_atual * acao["quantidade"]

        total_atual_acoes += valor_atual
        total_investido_acoes += acao["custo_total"]

        detalhes_acoes.append({
            "ticker": acao["ticker"],
            "quantidade": acao["quantidade"],
            "valor_investido": acao["custo_total"],
            "valor_atual": valor_atual,
            "lucro_prejuizo": valor_atual - acao["custo_total"]
        })
        

    total_investido = total_fixo + total_investido_acoes
    total_atual = patrimonio_total

    retorno_total = round((total_atual - total_investido), 2)
    retorno_percentual = round((retorno_total / total_investido) * 100, 2)

    return {
        "cpf": cpf,
        "patrimonio_total": patrimonio_total,
        "total_investido": total_investido,
        "retorno_total": retorno_total,
        "retorno_percentual": retorno_percentual,
        "renda_fixa_total": total_fixo,
        "acoes_total_atual": total_atual_acoes,
        "acoes_detalhes": detalhes_acoes
    }

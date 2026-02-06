from ..client.client_api import (
    buscar_cotacao_atual,
    buscar_historico_12m
)

from ..client.client_invest import (
    buscar_cliente_por_cpf_ms1,
    listar_investimentos_cliente_ms1,
    buscar_investidor_ms1
)



def normalizar_ticker(ticker):
    ticker = ticker.upper()

    if "." not in ticker and ticker.endswith(("3","4","11")):
        ticker += ".SA"

    return ticker




def calcular_rentabilidade_historica(historico):
    preco_inicial = round(historico[0], 2)
    preco_final = round(historico[-1], 2)

    rentabilidade = ((preco_final - preco_inicial) / preco_inicial) * 100
    return round(rentabilidade, 2)


# ================================
# ANALISE MERCADO
# ================================
def analise_mercado_service(ticker):

    ticker = normalizar_ticker(ticker)

    atual = buscar_cotacao_atual(ticker)
    if "erro" in atual:
        return atual

    historico = buscar_historico_12m(ticker)
    if "erro" in historico:
        return historico

    if len(historico) < 2:
        return {"erro": "Histórico insuficiente para análise"}

    rentabilidade = calcular_rentabilidade_historica(historico)

    return {
        "ticker": ticker,
        "preco_atual": round(atual["preco_atual"], 2),
        "preco_12m_inicial": round(historico[0], 2),
        "preco_12m_final": round(historico[-1], 2),
        "rentabilidade_12m_percentual": rentabilidade
    }


# ================================
# ANALISE CARTEIRA
# ================================
def analise_carteira_service(cpf):

    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return cliente

    id_cliente = cliente["id"]

    investimentos = listar_investimentos_cliente_ms1(id_cliente)
    if "erro" in investimentos or len(investimentos) == 0:
        return {"erro": "Cliente não possui investimentos"}

    investidor = buscar_investidor_ms1(id_cliente)
    if "erro" in investidor:
        return investidor

    perfil = investidor.get("perfil_investidor")
    patrimonio_total = float(investidor.get("patrimonio_total", 0))

    total_investido = sum(inv["valor_investido"] for inv in investimentos)

    return {
        "cpf": cpf,
        "perfil": perfil,
        "investimentos": investimentos,
        "total_investido": total_investido,
        "patrimonio_total": patrimonio_total
    }


# ================================
# PROJEÇÃO RETORNO
# ================================
def projecao_retorno_service(cpf):

    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return cliente

    id_cliente = cliente["id"]
    investidor = buscar_investidor_ms1(id_cliente)

    if "erro" in investidor:
        return investidor

    perfil = investidor["perfil_investidor"]
    patrimonio_atual = float(investidor.get("patrimonio_total", 0))

    taxas = {
        "conservador": 0.08,
        "moderado": 0.12,
        "arrojado": 0.18
    }

    taxa = taxas.get(perfil)

    if taxa is None:
        return {"erro": "Perfil de investidor inválido"}

    retorno_anual = round(patrimonio_atual * taxa, 2)

    return {
        "cpf": cpf,
        "perfil": perfil,
        "patrimonio_atual": patrimonio_atual,
        "taxa_perfil": taxa,
        "projecao_retorno_anual": retorno_anual
    }

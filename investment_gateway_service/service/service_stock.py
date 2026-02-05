from ..client.client_invest import (
    buscar_cliente_por_cpf_ms1,
    buscar_investidor_ms1,
    atualizar_investidor_ms1
)
from ..client.client_api import (
    criar_investimento_api_ms1,
    listar_investimentos_api_ms1,
    buscar_investimento_api_ms1,
    atualizar_investimento_api_ms1,
    registrar_operacao_api_ms1,
    buscar_cotacao_atual
)


# ================================
# COMPRA DE AÇÕES
# ================================
def comprar_acoes_service(cpf, ticker, quantidade=None, valor_investir=None):
    # Buscar cliente
    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return cliente
    
    id_cliente = cliente["id"]

    # Verificar se é investidor
    investidor = buscar_investidor_ms1(id_cliente)
    if "erro" in investidor or investidor.get("perfil_investidor") is None:
        return {"erro": "Cliente não é investidor"}

    patrimonio_atual = float(investidor["patrimonio_total"])

    # Buscar preço no mercado
    dados_mercado = buscar_cotacao_atual(ticker)
    if "erro" in dados_mercado:
        return dados_mercado

    preco_unitario = round(dados_mercado["preco_atual"], 2)

    # -----------------------------------------
    # COMPRA POR VALOR (ex: investir 300 reais)
    # -----------------------------------------
    if valor_investir is not None:
        try:
            valor_investir = float(valor_investir)
        except:
            return {"erro": "valor_investir deve ser numérico"}

        if valor_investir <= 0:
            return {"erro": "valor_investir deve ser maior que zero"}

        if valor_investir > patrimonio_atual:
            return {"erro": "Patrimônio insuficiente"}

        quantidade = int(valor_investir // preco_unitario)

        if quantidade <= 0:
            return {"erro": "Valor insuficiente para comprar ao menos 1 ação"}

        custo_total = round(quantidade * preco_unitario, 2)

    # -----------------------------------------
    # COMPRA POR QUANTIDADE (ex: comprar 10 ações)
    # -----------------------------------------
    elif quantidade is not None:
        try:
            quantidade = int(quantidade)
        except:
            return {"erro": "quantidade deve ser um número inteiro"}

        if quantidade <= 0:
            return {"erro": "A quantidade deve ser maior que zero"}

        custo_total = round(preco_unitario * quantidade, 2)

        if custo_total > patrimonio_atual:
            return {"erro": "Patrimônio insuficiente"}

    else:
        return {"erro": "Envie 'quantidade' OU 'valor_investir'"}

    # Criar investimento no MS1
    dados_investimento = {
        "cliente_id": id_cliente,
        "ticker": ticker.upper(),
        "quantidade": quantidade,
        "preco_unitario": preco_unitario,
        "custo_total": custo_total
    }

    resp = criar_investimento_api_ms1(dados_investimento)

    # Registrar operação (histórico)
    registrar_operacao_api_ms1({
        "cliente_id": id_cliente,
        "ticker": ticker.upper(),
        "tipo": "compra",
        "quantidade": quantidade,
        "preco_unitario": preco_unitario,
        "custo_total": custo_total
    })

    # Atualizar patrimônio
    novo_patrimonio = patrimonio_atual - custo_total
    atualizar_investidor_ms1(id_cliente, {
        "perfil_investidor": investidor["perfil_investidor"],
        "patrimonio_total": novo_patrimonio,
        "data_cadastro": investidor["data_cadastro"]
    })

    return {
        "msg": "Compra realizada com sucesso",
        "ticker": ticker.upper(),
        "quantidade_comprada": quantidade,
        "preco_unitario": preco_unitario,
        "custo_total": custo_total,
        "patrimonio_restante": novo_patrimonio,
        "response_ms1": resp
    }



# ================================
# VENDA DE AÇÕES
# ================================
def vender_acoes_service(cpf, id_investimento, quantidade):
    # Buscar cliente
    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return cliente
    
    id_cliente = cliente["id"]

    # Buscar investimento
    investimento = buscar_investimento_api_ms1(id_investimento)
    if "erro" in investimento:
        return investimento

    if investimento["cliente_id"] != id_cliente:
        return {"erro": "Este investimento não pertence a este cliente"}

    quantidade_atual = float(investimento["quantidade"])

    try:
        quantidade = int(quantidade)
    except:
        return {"erro": "quantidade deve ser um número inteiro"}

    if quantidade <= 0 or quantidade > quantidade_atual:
        return {"erro": "quantidade inválida para venda"}

    ticker = investimento["ticker"]
    preco_unitario_medio = float(investimento["preco_unitario"])

    # Buscar preço atual no mercado
    dados_mercado = buscar_cotacao_atual(ticker)
    if "erro" in dados_mercado:
        return dados_mercado

    preco_atual = round(dados_mercado["preco_atual"], 2)

    valor_recebido = round(quantidade * preco_atual, 2)

    nova_quantidade = quantidade_atual - quantidade
    novo_custo_total = round(nova_quantidade * preco_unitario_medio, 2)

    # Atualizar investimento no MS1
    atualizar_investimento_api_ms1(id_investimento, {
        "quantidade": nova_quantidade,
        "custo_total": novo_custo_total
    })

    # Registrar operação
    registrar_operacao_api_ms1({
        "cliente_id": id_cliente,
        "ticker": ticker.upper(),
        "tipo": "venda",
        "quantidade": quantidade,
        "preco_unitario": preco_atual,
        "custo_total": valor_recebido
    })

    # Atualizar patrimônio
    investidor = buscar_investidor_ms1(id_cliente)
    novo_patrimonio = float(investidor["patrimonio_total"]) + valor_recebido

    atualizar_investidor_ms1(id_cliente, {
        "perfil_investidor": investidor["perfil_investidor"],
        "patrimonio_total": novo_patrimonio,
        "data_cadastro": investidor["data_cadastro"]
    })

    return {
        "msg": "Venda realizada com sucesso",
        "ticker": ticker.upper(),
        "quantidade_vendida": quantidade,
        "preco_unitario_atual": preco_atual,
        "valor_recebido": valor_recebido,
        "novo_patrimonio": novo_patrimonio
    }
# ================================
# LISTAR AÇÕES DO CLIENTE
# ================================
def listar_acoes_cliente_service(cpf):

    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return []

    id_cliente = cliente["id"]

    investimentos = listar_investimentos_api_ms1(id_cliente)

    if "erro" in investimentos:
        return []

    # filtrar apenas investimentos que possuem ticker (ações)
    acoes = [inv for inv in investimentos if inv.get("ticker")]

    return acoes

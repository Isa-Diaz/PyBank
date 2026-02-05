from datetime import datetime

from ..client.client_invest import (
    buscar_cliente_por_cpf_ms1,
    buscar_investidor_ms1,
    criar_investidor_ms1,
    atualizar_investidor_ms1,
    criar_investimento_ms1,
    listar_investimentos_cliente_ms1,
    deletar_investimento_ms1,
    buscar_investimento_ms1,
    atualizar_investimento_ms1,
    buscar_cliente_por_id_ms1
)

def validar_perfil(perfil):
    perfis_validos = ["conservador", "moderado", "arrojado"]

    if not perfil:
        return None, "Perfil é obrigatório"

    perfil = str(perfil).lower()

    if perfil not in perfis_validos:
        return None, f"Perfil inválido. Use: {perfis_validos}"

    return perfil, None

def validar_patrimonio(patrimonio):
    try:
        patrimonio = float(patrimonio)
        if patrimonio <= 0:
            return None, "Patrimônio inicial deve ser maior que zero"
        return patrimonio, None
    except:
        return None, "O patrimônio inicial deve ser numérico"

def validar_valor(valor):
    try:
        v = float(valor)
        if v <= 0:
            return None, "O valor do investimento deve ser maior que zero"
        return v, None
    except:
        return None, "valor_investido deve ser numérico"

def criar_investidor_service(cpf, perfil, patrimonio_inicial):

    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return cliente
    if cliente["correntista"] != 1:
        return {"erro": "Apenas correntistas podem se tornar investidores"}

    id_cliente = cliente["id"]

    investidor = buscar_investidor_ms1(id_cliente)

    if "erro" not in investidor and investidor.get("perfil_investidor") is not None:
        return {"erro": "Cliente já é investidor"}

    perfil_validado, erro = validar_perfil(perfil)
    if erro:
        return {"erro": erro}

    patrimonio, erro = validar_patrimonio(patrimonio_inicial)
    if erro:
        return {"erro": erro}

    dados = {
        "perfil_investidor": perfil_validado,
        "patrimonio_total": patrimonio,
        "data_cadastro": datetime.now().strftime("%Y-%m-%d")
    }

    resposta = criar_investidor_ms1(id_cliente, dados)

    return {
        "msg": "Investidor criado com sucesso",
        "cpf": cpf,
        "id_cliente": id_cliente,
        "perfil": perfil_validado,
        "patrimonio_inicial": patrimonio,
        "data_cadastro": dados["data_cadastro"],
        "ms1_response": resposta
    }

def criar_investimento_fixo_service(cpf, valor_investido):

   
    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return cliente
    
    if cliente["correntista"] != 1:
        return {"erro": "Apenas correntistas podem fazer investimentos"}
    id_cliente = cliente["id"]
    investidor = buscar_investidor_ms1(id_cliente)
    if "erro" in investidor or investidor.get("perfil_investidor") is None:
        return {"erro": "Cliente não é investidor"}

    perfil = investidor["perfil_investidor"]    
    valor, erro = validar_valor(valor_investido)
    if erro:
        return {"erro": erro}

    patrimonio_atual = float(investidor.get("patrimonio_total", 0))
    taxas = {
        "conservador": 0.08,
        "moderado": 0.12,
        "arrojado": 0.18
    }

    if perfil not in taxas:
        return {"erro": "Perfil inválido para cálculo de rentabilidade"}

    taxa = taxas[perfil]
    rentabilidade = valor * taxa

    investimento = {
        "cliente_id": id_cliente,
        "tipo_investimento": "renda_fixa",
        "valor_investido": valor,
        "data_aplicacao": datetime.now().strftime("%Y-%m-%d"),
        "rentabilidade": rentabilidade,
        "ativo": 1
    }

    resp = criar_investimento_ms1(investimento)
    novo_patrimonio = patrimonio_atual + valor

    atualizar_investidor_ms1(id_cliente, {
        "patrimonio_total": novo_patrimonio,
        "perfil_investidor": perfil,
        "data_cadastro": investidor.get("data_cadastro")
    })

    return {
        "msg": "Investimento fixo criado com sucesso",
        "cpf": cpf,
        "valor_investido": valor,
        "rentabilidade_prevista": rentabilidade,
        "novo_patrimonio": novo_patrimonio,
        "ms1_response": resp
    }

def listar_investimentos_service(cpf):
    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return cliente
    if cliente["correntista"] != 1:
        return {"erro": "Apenas correntistas podem ter investimentos"}
    id_cliente = cliente["id"]
    investidor = buscar_investidor_ms1(id_cliente)
    if "erro" in investidor or investidor.get("perfil_investidor") is None:
        return {"erro": "Cliente não é investidor"}
   
    lista = listar_investimentos_cliente_ms1(id_cliente)

    if "erro" in lista:
        return lista
    return {
        "cpf": cpf,
        "id_cliente": id_cliente,
        "investimentos": lista
    }

def patrimonio_service(cpf):

    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return cliente

    if cliente["correntista"] != 1:
        return {"erro": "Apenas correntistas podem ter patrimônio"}

    id_cliente = cliente["id"]

    investidor = buscar_investidor_ms1(id_cliente)
    if "erro" in investidor or investidor.get("perfil_investidor") is None:
        return {"erro": "Cliente não é investidor"}

    patrimonio_total = float(investidor.get("patrimonio_total", 0))

    investimentos = listar_investimentos_cliente_ms1(id_cliente)
    if "erro" in investimentos:
        return investimentos

    # ===============================
    # CALCULAR RENTABILIDADE
    # ===============================

    total_investido = 0
    total_rentabilidade = 0

    for inv in investimentos:
        total_investido += float(inv.get("valor_investido", 0))
        total_rentabilidade += float(inv.get("rentabilidade", 0))

    retorno_percentual = 0

    if total_investido > 0:
        retorno_percentual = (total_rentabilidade / total_investido) * 100

    return {
        "cpf": cpf,
        "perfil": investidor["perfil_investidor"],
        "patrimonio_total": patrimonio_total,
        "retorno_percentual": round(retorno_percentual, 2),
        "quantidade_investimentos": len(investimentos),
        "detalhes_investimentos": investimentos
    }


def deletar_investimento_service(id_investimento):

    resp = deletar_investimento_ms1(id_investimento)

    if "erro" in resp:
        return resp

    return {
        "msg": "Investimento deletado com sucesso",
        "id_investimento": id_investimento
    }

def aporte_service(cpf, id_investimento, valor):

    # -------- validar valor --------
    try:
        valor = float(valor)
        if valor <= 0:
            return {"erro": "O valor deve ser maior que zero"}
    except:
        return {"erro": "Valor deve ser numérico"}

    # -------- buscar cliente pelo cpf --------
    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return cliente

    id_cliente = cliente["id"]

    # -------- buscar investimento --------
    investimento = buscar_investimento_ms1(id_investimento)
    if "erro" in investimento:
        return investimento

    # -------- validar dono do investimento --------
    if investimento["cliente_id"] != id_cliente:
        return {"erro": "Investimento não pertence a este cliente"}

    # -------- validar investidor --------
    investidor = buscar_investidor_ms1(id_cliente)
    if "erro" in investidor or investidor.get("perfil_investidor") is None:
        return {"erro": "Cliente não é investidor"}

    # -------- atualizar investimento --------
    valor_atual = float(investimento["valor_investido"])
    novo_valor = valor_atual + valor

    resp_inv = atualizar_investimento_ms1(
        id_investimento,
        {"valor_investido": novo_valor}
    )

    # -------- atualizar patrimônio --------
    patrimonio_atual = float(investidor.get("patrimonio_total", 0))
    patrimonio_novo = patrimonio_atual + valor

    atualizar_investidor_ms1(id_cliente, {
        "patrimonio_total": patrimonio_novo,
        "perfil_investidor": investidor["perfil_investidor"],
        "data_cadastro": investidor.get("data_cadastro")
    })

    return {
        "msg": "Aporte realizado com sucesso",
        "id_investimento": id_investimento,
        "antes": valor_atual,
        "depois": novo_valor,
        "patrimonio_novo": patrimonio_novo,
        "ms1": resp_inv
    }
def resgate_service(cpf, id_investimento, valor):

    # -------- validar valor --------
    try:
        valor = float(valor)
        if valor <= 0:
            return {"erro": "O valor deve ser maior que zero"}
    except:
        return {"erro": "Valor deve ser numérico"}

    # -------- buscar cliente --------
    cliente = buscar_cliente_por_cpf_ms1(cpf)
    if "erro" in cliente:
        return cliente

    id_cliente = cliente["id"]

    # -------- buscar investimento --------
    investimento = buscar_investimento_ms1(id_investimento)
    if "erro" in investimento:
        return investimento

    # -------- validar dono --------
    if investimento["cliente_id"] != id_cliente:
        return {"erro": "Investimento não pertence a este cliente"}

    # -------- validar investidor --------
    investidor = buscar_investidor_ms1(id_cliente)
    if "erro" in investidor or investidor.get("perfil_investidor") is None:
        return {"erro": "Cliente não é investidor"}

    valor_atual = float(investimento["valor_investido"])

    if valor > valor_atual:
        return {"erro": "Não é possível resgatar mais do que o valor investido"}

    # -------- atualizar investimento --------
    novo_valor = valor_atual - valor

    resp_inv = atualizar_investimento_ms1(
        id_investimento,
        {"valor_investido": novo_valor}
    )

    # -------- atualizar patrimônio --------
    patrimonio_atual = float(investidor.get("patrimonio_total", 0))
    patrimonio_novo = patrimonio_atual - valor

    atualizar_investidor_ms1(id_cliente, {
        "patrimonio_total": patrimonio_novo,
        "perfil_investidor": investidor["perfil_investidor"],
        "data_cadastro": investidor.get("data_cadastro")
    })

    return {
        "msg": "Resgate realizado com sucesso",
        "id_investimento": id_investimento,
        "antes": valor_atual,
        "depois": novo_valor,
        "patrimonio_novo": patrimonio_novo,
        "ms1": resp_inv
    }

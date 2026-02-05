from ..client.client_access import (
    criar_cliente,
    buscar_cliente_por_cpf,
    atualizar_cliente_por_cpf,
    criar_transacao,
    buscar_user_por_email,
    buscar_user_telefone,
    login_ms1,
    alterar_senha_ms1
)

from ..client.adm_access import listar_transacoes_por_id


# ---------------- TRATADOR PADRÃO ----------------

def ler_resposta(resp):
    if not resp:
        return {"erro": "MS1 fora do ar"}, 500

    if resp.status_code == 404:
        return {}, 404

    try:
        return resp.json(), resp.status_code
    except:
        return {"erro": resp.text}, resp.status_code


# ---------------- SCORE ----------------

def calcular_score(saldo):
    return saldo * 0.1 if saldo > 0 else 0


# ---------------- VALIDAÇÕES ----------------

def processar_dados(dados):
    if not dados.get("nome") or dados["nome"].strip() == "":
        return {"erro": "Nome é obrigatório", "valido": False}

    cpf = str(dados.get("cpf", "")).strip()
    if not cpf.isdigit() or len(cpf) != 11:
        return {"erro": "CPF deve conter 11 números", "valido": False}

    resp, status = ler_resposta(buscar_cliente_por_cpf(cpf))
    if status == 200:
        return {"erro": "CPF já cadastrado", "valido": False}

    email = dados.get("email", "").strip()
    if not email:
        return {"erro": "Email é obrigatório", "valido": False}

    resp, status = ler_resposta(buscar_user_por_email(email))
    if status == 200:
        return {"erro": "Email já cadastrado", "valido": False}

    telefone = str(dados.get("telefone", "")).strip()
    if not telefone.isdigit() or len(telefone) != 11:
        return {"erro": "Telefone deve conter 11 números", "valido": False}

    resp, status = ler_resposta(buscar_user_telefone(telefone))
    if status == 200:
        return {"erro": "Telefone já cadastrado", "valido": False}

    senha = dados.get("senha", "").strip()
    if not senha:
        return {"erro": "Senha é obrigatória", "valido": False}

    return {
        "valido": True,
        "dados": {
            "nome": dados["nome"].strip(),
            "cpf": cpf,
            "email": email,
            "telefone": telefone,
            "admin": dados.get("admin", 0),
            "senha": senha
        }
    }


def processar_correntista(dados):
    correntista = bool(dados.get("correntista", False))
    try:
        saldo_raw = float(dados.get("saldo_cc", 0))
    except:
        return {"erro": "saldo_cc deve ser numérico"}

    if not correntista and saldo_raw > 0:
        return {"erro": "Não correntista não pode iniciar com saldo"}
    if saldo_raw < 0:
        return {"erro": "Saldo inicial não pode ser negativo"}

    saldo_final = saldo_raw if correntista else 0
    return {
        "correntista": int(correntista),
        "saldo_cc": saldo_final,
        "score_credito": calcular_score(saldo_final)
    }


# ---------------- CREATE ----------------

def criar_cliente_service(dados):
    validacao = processar_dados(dados)
    if not validacao["valido"]:
        return validacao, 400

    correntista = processar_correntista(dados)
    if "erro" in correntista:
        return correntista, 400

    dados_final = {**validacao["dados"], **correntista}
    resp = criar_cliente(dados_final)
    return ler_resposta(resp)


# ---------------- UPDATE ----------------

def atualizar_cliente_service(cpf, dados):
    resp = buscar_cliente_por_cpf(cpf)
    cliente, status = ler_resposta(resp)
    if status != 200:
        return {"erro": "Cliente não encontrado"}, 404

    bloqueados = ["cpf", "saldo_cc", "score_credito", "admin"]
    if any(k in dados for k in bloqueados):
        return {"erro": "Campos não permitidos para atualização"}, 400

    # valida duplicidade de email/telefone
    if "email" in dados:
        resp_email, status_email = ler_resposta(buscar_user_por_email(dados["email"]))
        if status_email == 200 and dados["email"] != cliente["email"]:
            return {"erro": "Email já cadastrado"}, 400
    if "telefone" in dados:
        resp_tel, status_tel = ler_resposta(buscar_user_telefone(dados["telefone"]))
        if status_tel == 200 and dados["telefone"] != cliente["telefone"]:
            return {"erro": "Telefone já cadastrado"}, 400

    resp_update, status_update = ler_resposta(atualizar_cliente_por_cpf(cpf, dados))
    if status_update != 200:
        return {"erro": "Falha ao atualizar no MS1"}, 500

    cliente_atualizado, _ = ler_resposta(buscar_cliente_por_cpf(cpf))
    return {"msg": "Cliente atualizado com sucesso", **cliente_atualizado}, 200


# ---------------- OPERACOES ----------------

def validar_operacao(dados):
    if dados.get("tipo") not in ["saque", "deposito"]:
        return "Tipo inválido"
    try:
        valor = float(dados.get("valor"))
        if valor <= 0:
            return "Valor deve ser maior que zero"
    except:
        return "Valor inválido"
    return None


def operacao_service(cpf, dados):
    erro = validar_operacao(dados)
    if erro:
        return {"erro": erro}, 400

    resp = buscar_cliente_por_cpf(cpf)
    cliente, status = ler_resposta(resp)
    if status != 200:
        return {"erro": "Cliente não encontrado"}, 404
    if not cliente["correntista"]:
        return {"erro": "Cliente não é correntista"}, 400

    saldo = cliente["saldo_cc"]
    valor = float(dados["valor"])
    if dados["tipo"] == "saque" and saldo < valor:
        return {"erro": "Saldo insuficiente"}, 400

    novo_saldo = saldo + valor if dados["tipo"] == "deposito" else saldo - valor
    novo_score = calcular_score(novo_saldo)

    resp_update, status_update = ler_resposta(atualizar_cliente_por_cpf(cpf, {
        "saldo_cc": novo_saldo,
        "score_credito": novo_score
    }))
    if status_update != 200:
        return {"erro": "Falha ao atualizar saldo no MS1"}, 500

    criar_transacao({
        "cliente_id": cliente["id"],
        "tipo": dados["tipo"],
        "valor": valor,
        "descricao": f"Operação de {dados['tipo']}"
    })

    return {"msg": "Operação realizada", "saldo_cc": novo_saldo, "score_credito": novo_score}, 200


# ---------------- TRANSACOES ----------------

def listar_transacoes_cpf(cpf):
    resp = buscar_cliente_por_cpf(cpf)
    cliente, status = ler_resposta(resp)
    if status != 200:
        return {"erro": "Cliente não encontrado"}, 404

    return listar_transacoes_por_id(cliente["id"])


# ---------------- LOGIN ----------------

def login_service(cpf, senha):
    resp = login_ms1(cpf, senha)
    resultado, status = ler_resposta(resp)
    if status == 200:
        return resultado, 200
    if status == 401:
        return {"erro": "Senha incorreta"}, 401
    if status == 404:
        return {"erro": "Cliente não encontrado"}, 404
    return {"erro": "Falha no login"}, status


# ---------------- ALTERAR SENHA ----------------

def alterar_senha_service(cpf, senha_atual, nova_senha):
    resp = alterar_senha_ms1(cpf, senha_atual, nova_senha)
    return ler_resposta(resp)


# ---------------- BUSCAR ----------------

def buscar_cliente_service(cpf):
    resp = buscar_cliente_por_cpf(cpf)
    return ler_resposta(resp)


# ---------------- DELETAR ----------------
def deletar_cliente_service(cpf):
    resp = buscar_cliente_por_cpf(cpf)
    cliente, status = ler_resposta(resp)

    if status != 200:
        return {"erro": "Cliente não encontrado"}, 404

    # ❗ regra nova
    if cliente["saldo_cc"] != 0:
        return {"erro": "Não é possível excluir conta com saldo diferente de zero"}, 400

    # cliente comum NUNCA pode excluir admin
    if cliente["admin"] == 1:
        return {"erro": "Administradores não podem excluir a si mesmos"}, 403

    from ..client.adm_access import deletar_cliente_por_id
    resp_delete = deletar_cliente_por_id(cliente["id"])
    return ler_resposta(resp_delete)
    
from ..client.client_access import (
    criar_cliente,
    buscar_cliente_por_cpf,
    atualizar_cliente_por_cpf,
    criar_transacao,
    buscar_user_por_email,
    buscar_user_telefone,
    login_ms1,
    alterar_senha_ms1
)

from ..client.adm_access import listar_transacoes_por_id


# ---------------- TRATADOR PADRÃO ----------------

def ler_resposta(resp):
    if not resp:
        return {"erro": "MS1 fora do ar"}, 500

    if resp.status_code == 404:
        return {}, 404

    try:
        return resp.json(), resp.status_code
    except:
        return {"erro": resp.text}, resp.status_code


# ---------------- SCORE ----------------

def calcular_score(saldo):
    return saldo * 0.1 if saldo > 0 else 0


# ---------------- VALIDAÇÕES ----------------

def processar_dados(dados):
    if not dados.get("nome") or dados["nome"].strip() == "":
        return {"erro": "Nome é obrigatório", "valido": False}

    cpf = str(dados.get("cpf", "")).strip()
    if not cpf.isdigit() or len(cpf) != 11:
        return {"erro": "CPF deve conter 11 números", "valido": False}

    resp, status = ler_resposta(buscar_cliente_por_cpf(cpf))
    if status == 200:
        return {"erro": "CPF já cadastrado", "valido": False}

    email = dados.get("email", "").strip()
    if not email:
        return {"erro": "Email é obrigatório", "valido": False}

    resp, status = ler_resposta(buscar_user_por_email(email))
    if status == 200:
        return {"erro": "Email já cadastrado", "valido": False}

    telefone = str(dados.get("telefone", "")).strip()
    if not telefone.isdigit() or len(telefone) != 11:
        return {"erro": "Telefone deve conter 11 números", "valido": False}

    resp, status = ler_resposta(buscar_user_telefone(telefone))
    if status == 200:
        return {"erro": "Telefone já cadastrado", "valido": False}

    senha = dados.get("senha", "").strip()
    if not senha:
        return {"erro": "Senha é obrigatória", "valido": False}

    return {
        "valido": True,
        "dados": {
            "nome": dados["nome"].strip(),
            "cpf": cpf,
            "email": email,
            "telefone": telefone,
            "admin": dados.get("admin", 0),
            "senha": senha
        }
    }


def processar_correntista(dados):
    correntista = bool(dados.get("correntista", False))
    try:
        saldo_raw = float(dados.get("saldo_cc", 0))
    except:
        return {"erro": "saldo_cc deve ser numérico"}

    if not correntista and saldo_raw > 0:
        return {"erro": "Não correntista não pode iniciar com saldo"}
    if saldo_raw < 0:
        return {"erro": "Saldo inicial não pode ser negativo"}

    saldo_final = saldo_raw if correntista else 0
    return {
        "correntista": int(correntista),
        "saldo_cc": saldo_final,
        "score_credito": calcular_score(saldo_final)
    }


# ---------------- CREATE ----------------

def criar_cliente_service(dados):
    validacao = processar_dados(dados)
    if not validacao["valido"]:
        return validacao, 400

    correntista = processar_correntista(dados)
    if "erro" in correntista:
        return correntista, 400

    dados_final = {**validacao["dados"], **correntista}
    resp = criar_cliente(dados_final)
    return ler_resposta(resp)


# ---------------- UPDATE ----------------

def atualizar_cliente_service(cpf, dados):
    resp = buscar_cliente_por_cpf(cpf)
    cliente, status = ler_resposta(resp)
    if status != 200:
        return {"erro": "Cliente não encontrado"}, 404

    bloqueados = ["cpf", "saldo_cc", "score_credito", "admin"]
    if any(k in dados for k in bloqueados):
        return {"erro": "Campos não permitidos para atualização"}, 400

    # valida duplicidade de email/telefone
    if "email" in dados:
        resp_email, status_email = ler_resposta(buscar_user_por_email(dados["email"]))
        if status_email == 200 and dados["email"] != cliente["email"]:
            return {"erro": "Email já cadastrado"}, 400
    if "telefone" in dados:
        resp_tel, status_tel = ler_resposta(buscar_user_telefone(dados["telefone"]))
        if status_tel == 200 and dados["telefone"] != cliente["telefone"]:
            return {"erro": "Telefone já cadastrado"}, 400

    resp_update, status_update = ler_resposta(atualizar_cliente_por_cpf(cpf, dados))
    if status_update != 200:
        return {"erro": "Falha ao atualizar no MS1"}, 500

    cliente_atualizado, _ = ler_resposta(buscar_cliente_por_cpf(cpf))
    return {"msg": "Cliente atualizado com sucesso", **cliente_atualizado}, 200


# ---------------- OPERACOES ----------------

def validar_operacao(dados):
    if dados.get("tipo") not in ["saque", "deposito"]:
        return "Tipo inválido"
    try:
        valor = float(dados.get("valor"))
        if valor <= 0:
            return "Valor deve ser maior que zero"
    except:
        return "Valor inválido"
    return None


def operacao_service(cpf, dados):
    erro = validar_operacao(dados)
    if erro:
        return {"erro": erro}, 400

    resp = buscar_cliente_por_cpf(cpf)
    cliente, status = ler_resposta(resp)
    if status != 200:
        return {"erro": "Cliente não encontrado"}, 404
    if not cliente["correntista"]:
        return {"erro": "Cliente não é correntista"}, 400

    saldo = cliente["saldo_cc"]
    valor = float(dados["valor"])
    if dados["tipo"] == "saque" and saldo < valor:
        return {"erro": "Saldo insuficiente"}, 400

    novo_saldo = saldo + valor if dados["tipo"] == "deposito" else saldo - valor
    novo_score = calcular_score(novo_saldo)

    resp_update, status_update = ler_resposta(atualizar_cliente_por_cpf(cpf, {
        "saldo_cc": novo_saldo,
        "score_credito": novo_score
    }))
    if status_update != 200:
        return {"erro": "Falha ao atualizar saldo no MS1"}, 500

    criar_transacao({
        "cliente_id": cliente["id"],
        "tipo": dados["tipo"],
        "valor": valor,
        "descricao": f"Operação de {dados['tipo']}"
    })

    return {"msg": "Operação realizada", "saldo_cc": novo_saldo, "score_credito": novo_score}, 200


# ---------------- TRANSACOES ----------------

def listar_transacoes_cpf(cpf):
    resp = buscar_cliente_por_cpf(cpf)
    cliente, status = ler_resposta(resp)
    if status != 200:
        return {"erro": "Cliente não encontrado"}, 404

    return listar_transacoes_por_id(cliente["id"])


# ---------------- LOGIN ----------------

def login_service(cpf, senha):
    resp = login_ms1(cpf, senha)
    resultado, status = ler_resposta(resp)
    if status == 200:
        return resultado, 200
    if status == 401:
        return {"erro": "Senha incorreta"}, 401
    if status == 404:
        return {"erro": "Cliente não encontrado"}, 404
    return {"erro": "Falha no login"}, status


# ---------------- ALTERAR SENHA ----------------

def alterar_senha_service(cpf, senha_atual, nova_senha):
    resp = alterar_senha_ms1(cpf, senha_atual, nova_senha)
    return ler_resposta(resp)


# ---------------- BUSCAR CLIENTE ----------------

def buscar_cliente_service(cpf):
    return ler_resposta(buscar_cliente_por_cpf(cpf))


# ---------------- DELETAR CLIENTE ----------------

def deletar_cliente_service(cpf):
    from ..client.adm_access import deletar_cliente_por_id

    resp = buscar_cliente_por_cpf(cpf)
    cliente, status = ler_resposta(resp)
    if status != 200:
        return {"erro": "Cliente não encontrado"}, 404

    resp_delete = deletar_cliente_por_id(cliente["id"])
    return ler_resposta(resp_delete)

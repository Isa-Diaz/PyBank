from ..client.adm_access import (
    listar_clientes,
    buscar_cliente_por_id,
    atualizar_cliente,
    listar_investidores,
    buscar_investidor_por_id,
    buscar_investidor_com_cliente,
    listar_transacoes_por_id,
    deletar_cliente,
    listar_investimentos
    
)

from ..client.client_access import buscar_cliente_por_cpf

def promover_para_admin(id_cliente):
    cliente = buscar_cliente_por_id(id_cliente)

    if "erro" in cliente:
        return cliente

    if cliente["admin"] == 1:
        return {"erro": "Este cliente já é administrador"}

    dados = {"admin": 1}
    return atualizar_cliente(id_cliente, dados)

def remover_admin(id_cliente):
    cliente = buscar_cliente_por_id(id_cliente)

    if "erro" in cliente:
        return cliente

    if cliente["admin"] == 0:
        return {"erro": "Este cliente não é administrador"}

    dados = {"admin": 0}
    return atualizar_cliente(id_cliente, dados)

def alterar_cpf_admin_service(id_cliente, novo_cpf):
    novo_cpf = str(novo_cpf).strip()

    if not novo_cpf.isdigit() or len(novo_cpf) != 11:
        return {"erro": "O novo CPF deve conter 11 números"}

    cliente = buscar_cliente_por_id(id_cliente)
    if "erro" in cliente:
        return cliente

    resultado = buscar_cliente_por_cpf(novo_cpf)
    if "id" in resultado and resultado["id"] != id_cliente:
        return {"erro": "Este CPF já está vinculado a outro cliente"}

    dados = {"cpf": novo_cpf}
    return atualizar_cliente(id_cliente, dados)


def atualizar_cliente_admin_service(id_cliente, dados):

    cliente = buscar_cliente_por_id(id_cliente)
    if "erro" in cliente:
        return cliente

    if "cpf" in dados:
        return alterar_cpf_admin_service(id_cliente, dados["cpf"])

    if "score_credito" in dados:
        return {"erro": "Score é calculado automaticamente"}

    if "saldo_cc" in dados:
        return {"erro": "Saldo não pode ser alterado diretamente"}

    if "correntista" in dados:
        if dados["correntista"] in (False, 0) and cliente["saldo_cc"] > 0:
            return {"erro": "Não é possível desativar correntista com saldo positivo"}

    return atualizar_cliente(id_cliente, dados)

def deletar_cliente_admin_service(id_cliente):

    cliente = buscar_cliente_por_id(id_cliente)
    if "erro" in cliente:
        return cliente

    if cliente["saldo_cc"] != 0:
        return {"erro": "Não é possível excluir conta com saldo diferente de zero"}

    return deletar_cliente(id_cliente)


def listar_todos_clientes_service():
    return listar_clientes()


def listar_todos_investidores_service():
    return listar_investidores()

def buscar_cliente_admin_service(id_cliente):
    return buscar_cliente_por_id(id_cliente)

def buscar_investidor_admin_service(id_cliente):
    return buscar_investidor_por_id(id_cliente)

def buscar_cliente_com_investidor_service(id_cliente):
    return buscar_investidor_com_cliente(id_cliente)

def listar_transacoes_admin_service(id_cliente):
    return listar_transacoes_por_id(id_cliente)

def listar_clientes_com_investimentos_service():
    clientes = listar_clientes()
    investidores = listar_investidores()
    investimentos = listar_investimentos()

    investidores_dict = {i["id_cliente"]: i for i in investidores}
    investimentos_por_cliente = {}
    for inv in investimentos:
        cid = inv["cliente_id"]
        investimentos_por_cliente.setdefault(cid, []).append(inv)
    resposta = []
    for c in clientes:
        if c["correntista"] != 1:
            continue
        id_cliente = c["id"]
        investidor = investidores_dict.get(id_cliente)
        perfil = None
        patrimonio = None
        qtd_invest = 0
        if investidor:
            perfil = investidor["perfil_investidor"]
            patrimonio = investidor["patrimonio_total"]
            qtd_invest = len(investimentos_por_cliente.get(id_cliente, []))
        resposta.append({
            "id": c["id"],
            "admin": c["admin"],
            "correntista": c["correntista"],
            "cpf": c["cpf"],
            "email": c["email"],
            "nome": c["nome"],
            "telefone": c["telefone"],
            "saldo_cc": c["saldo_cc"],
            "score_credito": c["score_credito"],
            "perfil": perfil,
            "patrimonio_total": patrimonio,
            "quantidade_investimentos": qtd_invest
        })
    return resposta
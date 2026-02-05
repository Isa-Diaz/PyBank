from flask import Blueprint, request, jsonify
from ..repository.database import(
    buscar_user_por_id,
    buscar_investidor_por_id,
    insert_investidor,
    insert_tipo_investimento,
    listar_investimentos,
    buscar_investimento_por_id,
    delete_investimento
)
invest_bp = Blueprint("investidor_investimento", __name__)

@invest_bp.route("/admin/investidor/<id_cliente>", methods=["POST"])
def criar_investidor(id_cliente):
    cliente = buscar_user_por_id(id_cliente)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    investidor = buscar_investidor_por_id(id_cliente)
    if investidor:
        return jsonify({"erro": "Cliente já é investidor"}), 400
    
    dados = request.get_json()
    perfil = dados.get("perfil_investidor")
    patrimonio = dados.get("patrimonio_total", 0)
    data = dados.get("data_cadastro")
    insert_investidor(id_cliente, perfil, patrimonio, data)
    return jsonify({
        "msg": "Investidor criado com sucesso",
        "id_cliente": id_cliente,
        "perfil_investidor": perfil,
        "patrimonio_total": patrimonio,
        "data_cadastro": data
    }), 201

    
@invest_bp.route("/admin/investimentos", methods=["POST"])
def criar_investimento():
    dados = request.get_json()
    id_cliente = dados.get("cliente_id")
    tipo = dados.get("tipo_investimento")
    valor = dados.get("valor_investido")
    data = dados.get("data_aplicacao")
    rentabilidade = dados.get("rentabilidade")
    ativo = dados.get("ativo", 1)
    cliente = buscar_user_por_id(id_cliente)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    investimento_id, _ = insert_tipo_investimento(
        id_cliente, tipo, valor, data, rentabilidade, ativo
    )
    return jsonify({
        "msg": "Investimento criado",
        "id_investimento": investimento_id,
        "cliente_id": id_cliente,
        "tipo_investimento": tipo,
        "valor_investido": valor,
        "data_aplicacao": data,
        "rentabilidade": rentabilidade,
        "ativo": ativo
    }), 201


@invest_bp.route("/admin/investimentos/<id_cliente>", methods=["GET"])
def listar_investimentos_cliente(id_cliente):
    investimentos = [
        inv for inv in listar_investimentos()
        if inv[1] == id_cliente
    ]
    lista = []
    for linha in investimentos:
        lista.append({
            "id_investimento": linha[0],
            "cliente_id": linha[1],
            "tipo_investimento": linha[2],
            "valor_investido": linha[3],
            "data_aplicacao": linha[4],
            "rentabilidade": linha[5],
            "ativo": linha[6],
        })
    return jsonify(lista), 200

@invest_bp.route("/admin/investidor/<id_cliente>", methods=["GET"])
def buscar_investidor(id_cliente):
    investidor = buscar_investidor_por_id(id_cliente)
    if not investidor:
        return jsonify({"erro": "Investidor não encontrado"}), 404

    return jsonify({
        "id_cliente": investidor[0],
        "perfil_investidor": investidor[1],
        "patrimonio_total": investidor[2],
        "data_cadastro": investidor[3]
    }), 200


@invest_bp.route("/admin/investimentos", methods=["GET"])
def listar_todos_investimentos():
    linhas = listar_investimentos()
    lista = []

    for linha in linhas:
        lista.append({
            "id_investimento": linha[0],
            "cliente_id": linha[1],
            "tipo_investimento": linha[2],
            "valor_investido": linha[3],
            "data_aplicacao": linha[4],
            "rentabilidade": linha[5],
            "ativo": linha[6],
        })

    return jsonify(lista), 200


from ..repository.database import atualizar_investimento

@invest_bp.route("/admin/investimentos/<id_investimento>", methods=["PATCH"])
def atualizar_investimento_controller(id_investimento):
    dados = request.get_json()

    investimento = buscar_investimento_por_id(id_investimento)
    if not investimento:
        return jsonify({"erro": "Investimento não encontrado"}), 404

    atualizar_investimento(
        id_investimento=id_investimento,
        cliente_id=dados.get("cliente_id"),
        tipo_investimento=dados.get("tipo_investimento"),
        valor_investido=dados.get("valor_investido"),
        data_aplicacao=dados.get("data_aplicacao"),
        rentabilidade=dados.get("rentabilidade"),
        ativo=dados.get("ativo")
    )

    return jsonify({"msg": "Investimento atualizado"}), 200

@invest_bp.route("/admin/investimentos/<id_investimento>", methods=["DELETE"])
def deletar_investimento(id_investimento):
    investimento = buscar_investimento_por_id(id_investimento)
    if not investimento:
        return jsonify({"erro": "Investimento não encontrado"}), 404
    delete_investimento(id_investimento)
    return jsonify({"msg": "Investimento deletado"}), 200
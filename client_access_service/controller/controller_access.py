from flask import Flask, request, jsonify
from flask_cors import CORS

from ..service.cliente_service_access import (
    criar_cliente_service,
    atualizar_cliente_service,
    operacao_service,
    listar_transacoes_cpf,
    login_service,
    alterar_senha_service,
    buscar_cliente_service,       
    deletar_cliente_service        
)

from ..service.adm_service_access import (
    listar_todos_clientes_service,
    listar_todos_investidores_service,
    buscar_cliente_admin_service,
    buscar_investidor_admin_service,
    buscar_cliente_com_investidor_service,
    listar_transacoes_admin_service,
    promover_para_admin,
    remover_admin,
    alterar_cpf_admin_service,
    atualizar_cliente_admin_service,
    deletar_cliente_admin_service,
    listar_clientes_com_investimentos_service
)

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)

# 🔒 BLINDAGEM DE STATUS HTTP DO MS2 INTEIRO
def response_padrao(retorno):
    if isinstance(retorno, tuple):
        return jsonify(retorno[0]), retorno[1]
    return jsonify(retorno), 200


# ================= CLIENTE =================

@app.route("/cliente", methods=["POST"])
def criar_cliente_controller():
    dados = request.get_json()
    return response_padrao(criar_cliente_service(dados))


@app.route("/cliente/<cpf>", methods=["GET"])
def buscar_cliente_controller(cpf):
    return response_padrao(buscar_cliente_service(cpf))


@app.route("/cliente/<cpf>", methods=["PATCH"])
def atualizar_cliente_controller(cpf):
    dados = request.get_json()
    return response_padrao(atualizar_cliente_service(cpf, dados))


@app.route("/cliente/<cpf>", methods=["DELETE"])
def deletar_cliente_controller(cpf):
    return response_padrao(deletar_cliente_service(cpf))


@app.route("/cliente/operacao/<cpf>", methods=["POST"])
def operacao_cliente_controller(cpf):
    dados = request.get_json()
    return response_padrao(operacao_service(cpf, dados))


@app.route("/cliente/transacoes/<cpf>", methods=["GET"])
def listar_transacoes_controller(cpf):
    return response_padrao(listar_transacoes_cpf(cpf))


# ================= ADMIN =================

@app.route("/admin/clientes", methods=["GET"])
def admin_listar_clientes():
    return response_padrao(listar_todos_clientes_service())


@app.route("/admin/clientes/<id_cliente>", methods=["GET"])
def admin_buscar_cliente(id_cliente):
    return response_padrao(buscar_cliente_admin_service(id_cliente))


@app.route("/admin/clientes/<id_cliente>", methods=["PATCH"])
def admin_atualizar_cliente(id_cliente):
    dados = request.get_json()
    return response_padrao(atualizar_cliente_admin_service(id_cliente, dados))


@app.route("/admin/clientes/<id_cliente>", methods=["DELETE"])
def admin_deletar_cliente(id_cliente):
    return response_padrao(deletar_cliente_admin_service(id_cliente))


@app.route("/admin/transacoes/<id_cliente>", methods=["GET"])
def admin_listar_transacoes(id_cliente):
    return response_padrao(listar_transacoes_admin_service(id_cliente))


@app.route("/admin/investidores", methods=["GET"])
def admin_listar_investidores():
    return response_padrao(listar_todos_investidores_service())


@app.route("/admin/investidor/<id_cliente>", methods=["GET"])
def admin_buscar_investidor(id_cliente):
    return response_padrao(buscar_investidor_admin_service(id_cliente))


@app.route("/admin/cliente-investidor/<id_cliente>", methods=["GET"])
def admin_buscar_cliente_com_investidor(id_cliente):
    return response_padrao(buscar_cliente_com_investidor_service(id_cliente))


@app.route("/admin/promover/<id_cliente>", methods=["POST"])
def admin_promover(id_cliente):
    return response_padrao(promover_para_admin(id_cliente))


@app.route("/admin/remover/<id_cliente>", methods=["POST"])
def admin_remover(id_cliente):
    return response_padrao(remover_admin(id_cliente))


@app.route("/admin/alterar-cpf/<id_cliente>", methods=["POST"])
def admin_alterar_cpf(id_cliente):
    novo_cpf = request.get_json().get("novo_cpf")
    return response_padrao(alterar_cpf_admin_service(id_cliente, novo_cpf))


@app.route("/admin/clientes/investimentos", methods=["GET"])
def admin_listar_clientes_com_investimentos():
    return response_padrao(listar_clientes_com_investimentos_service())


# ================= LOGIN / SENHA =================

@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    resultado = login_service(
        dados.get("cpf"),
        dados.get("senha")
    )
    return response_padrao(resultado)


@app.route("/alterar-senha", methods=["PATCH"])
def alterar_senha():
    dados = request.get_json()
    resultado = alterar_senha_service(
        dados.get("cpf"),
        dados.get("senha_atual"),
        dados.get("nova_senha")
    )
    return response_padrao(resultado)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"]
)
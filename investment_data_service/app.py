from flask import Flask
from .controller_storage.adm_controller import adm_bp
from .controller_storage.cliente_controller import cliente_bp
from .controller_storage.investiment_controller import invest_bp
from .controller_storage.api_controller import invest_api_bp


from .repository.database import (
    create_table_user,
    create_table_investidor,
    create_table_tipo_investimento,
    create_table_transacoes,
    create_table_investimentos_api,
    create_table_transacoes_api    
)

app = Flask(__name__)


# CRIA TODAS AS TABELAS CORRETAMENTE
create_table_user()
create_table_investidor()
create_table_tipo_investimento()
create_table_transacoes()
create_table_investimentos_api()
create_table_transacoes_api()


app.register_blueprint(adm_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(invest_bp)
app.register_blueprint(invest_api_bp)

# pragma: no cover
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)

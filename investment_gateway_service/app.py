from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

from .controller_invest.controller_invest_fixo import invest_fixo_bp
from .controller_invest.controller_invest_api import invest_api_bp
from .controller_invest.controller_stock import stock_bp
from .controller_invest.controller_analytics import analytics_bp
from .controller_invest.controller_graphics import graphics_bp   # <-- ADICIONAR AQUI

app.register_blueprint(invest_fixo_bp)
app.register_blueprint(invest_api_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(graphics_bp)   # <-- ADICIONAR AQUI

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5002)

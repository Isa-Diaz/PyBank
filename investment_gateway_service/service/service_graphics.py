import matplotlib
matplotlib.use("Agg")     # <-- ESSENCIAL

import io
import matplotlib.pyplot as plt
import seaborn as sns
from flask import send_file, jsonify
import numpy as np

from ..client.client_api import buscar_historico_12m, buscar_cotacao_atual


# ================================
# 1. GRÁFICO DE EVOLUÇÃO DE PREÇO
# ================================
def grafico_preco_service(ticker):

    historico = buscar_historico_12m(ticker)

    # 1) se API retornou erro:
    if isinstance(historico, dict) and "erro" in historico:
        return historico, 400

    # 2) se histórico é vazio:
    if not historico:
        return {"erro": "Sem dados suficientes para gerar o gráfico"}, 400

    # Plot seguro
    plt.figure(figsize=(10,5))
    sns.lineplot(x=list(range(len(historico))), y=historico)
    plt.title(f"Evolução de Preço — {ticker.upper()}")
    plt.xlabel("Dias (12 meses)")
    plt.ylabel("Preço de fechamento (R$)")
    plt.grid(True)

    # Salvar em memória
    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)

    return send_file(img, mimetype="image/png")


# ================================
# 2. GRÁFICO DE PROJEÇÃO MONTE CARLO
# ================================
def grafico_projecao_service(ticker):
    historico = buscar_historico_12m(ticker)

    # 1) se API retornou erro
    if isinstance(historico, dict) and "erro" in historico:
        return historico, 400

    # 2) se não há dados suficientes
    if not historico or len(historico) < 2:
        return {"erro": "Sem dados suficientes para gerar projeção"}, 400

    serie = np.array(historico)
    retornos = np.diff(serie) / serie[:-1]

    # 3) se retornos insuficientes
    if len(retornos) == 0:
        return {"erro": "Histórico muito curto para projeção"}, 400

    media = np.mean(retornos)
    vol = np.std(retornos)

    # Parâmetros da simulação
    dias = 252
    num_sim = 300
    simulations = np.zeros((dias, num_sim))
    ultimo_preco = serie[-1]

    for s in range(num_sim):
        preco = ultimo_preco
        for d in range(dias):
            preco *= (1 + np.random.normal(media, vol))
            simulations[d, s] = preco

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(simulations, color="blue", alpha=0.05)
    plt.title(f"Projeção de Preço — {ticker.upper()}")
    plt.xlabel("Dias (1 ano)")
    plt.ylabel("Simulação de Preço (R$)")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)

    return send_file(img, mimetype="image/png")

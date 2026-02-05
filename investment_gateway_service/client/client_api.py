import yfinance as yf
import requests
from .core import URL_MS1, resposta

def buscar_cotacao_atual(ticker):
    try:
        ativo = yf.Ticker(ticker)
        dados = ativo.history(period="1d")

        if dados.empty:
            return {"erro": "Ticker inválido ou sem dados"}

        preco = float(dados["Close"].iloc[-1])

        return {"ticker": ticker.upper(), "preco_atual": preco}

    except Exception as e:
        return {"erro": f"Erro ao acessar API externa: {str(e)}"}

def buscar_historico_12m(ticker):
    try:
        ativo = yf.Ticker(ticker)
        dados = ativo.history(period="1y")

        if dados.empty:
            return {"erro": "Ticker inválido ou sem dados"}

        return dados["Close"].tolist()

    except Exception as e:
        return {"erro": f"Erro ao acessar API externa: {str(e)}"}

def criar_investimento_api_ms1(dados):
    return resposta(requests.post(
        f"{URL_MS1}/api/acoes",
        json=dados
    ))
def listar_investimentos_api_ms1(cliente_id):
    return resposta(requests.get(
        f"{URL_MS1}/api/acoes/cliente/{cliente_id}"
    ))
def buscar_investimento_api_ms1(id_investimento):
    return resposta(requests.get(
        f"{URL_MS1}/api/acoes/{id_investimento}"
    ))
def atualizar_investimento_api_ms1(id_investimento, dados):
    return resposta(requests.patch(
        f"{URL_MS1}/api/acoes/{id_investimento}",
        json=dados
    ))
def registrar_operacao_api_ms1(dados):
    return resposta(requests.post(
        f"{URL_MS1}/api/acoes/transacao",
        json=dados
    ))
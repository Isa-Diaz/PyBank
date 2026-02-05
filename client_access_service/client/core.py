URL = "http://localhost:5000"

def resposta(result):
    try:
        return result.json()
    except ValueError:
        return {
            "erro": "Resposta inválida do microserviço",
            "raw": result.text,
            "status": result.status_code
        }

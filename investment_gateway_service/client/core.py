URL_MS1 = "http://localhost:5000"

def resposta(result):
    try:
        return result.json()
    except ValueError:
        return {
            "erro": "Resposta inválida do microserviço",
            "status": result.status_code,
            "raw": result.text
        }


{
  "openapi": "3.0.3",
  "info": {
    "title": "Microserviço de Investimentos MS3",
    "version": "1.0.0",
    "description": "API responsável por operações de investimentos, renda fixa, ações, projeções, análises e gráficos."
  },
  "servers": [
    {
      "url": "http://localhost:5002",
      "description": "Servidor principal do MS3"
    }
  ],
  "tags": [
    { "name": "Investidor", "description": "Gerenciamento de investidores" },
    { "name": "Renda Fixa", "description": "Investimentos de renda fixa" },
    { "name": "Ações", "description": "Compra e venda de ações" },
    { "name": "Patrimônio", "description": "Consulta de patrimônio" },
    { "name": "Análises", "description": "Análises de mercado e carteira" },
    { "name": "Analytics", "description": "Performance completa da carteira" },
    { "name": "Gráficos", "description": "Geração de gráficos financeiros" }
  ],
  "paths": {

    "/investidor": {
      "post": {
        "tags": ["Investidor"],
        "summary": "Cria um investidor",
        "description": "Converte um cliente correntista em investidor cadastrado.",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "cpf": { "type": "string" },
                  "perfil_investidor": { "type": "string", "enum": ["conservador","moderado","arrojado"] },
                  "patrimonio_inicial": { "type": "number" }
                },
                "required": ["cpf", "perfil_investidor", "patrimonio_inicial"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Investidor criado com sucesso.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/investimentos/fixo": {
      "post": {
        "tags": ["Renda Fixa"],
        "summary": "Cria investimento de renda fixa",
        "description": "Aplica um valor em um investimento de renda fixa baseado no perfil do investidor.",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "cpf": { "type": "string" },
                  "valor_investido": { "type": "number" }
                },
                "required": ["cpf", "valor_investido"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Investimento de renda fixa criado.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/investimentos/{cpf}": {
      "get": {
        "tags": ["Renda Fixa"],
        "summary": "Lista todos os investimentos de renda fixa do cliente",
        "parameters": [
          {
            "name": "cpf",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "Lista de investimentos retornada.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/patrimonio/{cpf}": {
      "get": {
        "tags": ["Patrimônio"],
        "summary": "Consulta o patrimônio total do investidor",
        "parameters": [
          {
            "name": "cpf",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "Patrimônio retornado.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/investimentos/{id_investimento}": {
      "delete": {
        "tags": ["Renda Fixa"],
        "summary": "Remove um investimento de renda fixa",
        "parameters": [
          {
            "name": "id_investimento",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "Investimento removido.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/investimentos/aporte/{id_investimento}": {
      "post": {
        "tags": ["Renda Fixa"],
        "summary": "Realiza um aporte em um investimento",
        "parameters": [
          {
            "name": "id_investimento",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "valor": { "type": "number" }
                },
                "required": ["valor"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Aporte realizado.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/investimentos/resgate/{id_investimento}": {
      "post": {
        "tags": ["Renda Fixa"],
        "summary": "Realiza um resgate parcial de um investimento",
        "parameters": [
          {
            "name": "id_investimento",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "valor": { "type": "number" }
                },
                "required": ["valor"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Resgate realizado.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/acoes/comprar": {
      "post": {
        "tags": ["Ações"],
        "summary": "Compra ações",
        "description": "Permite comprar ações por quantidade ou por valor total investido.",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "cpf": { "type": "string" },
                  "ticker": { "type": "string" },
                  "quantidade": { "type": "integer", "nullable": true },
                  "valor_investir": { "type": "number", "nullable": true }
                },
                "required": ["cpf", "ticker"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Compra realizada com sucesso.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/acoes/vender": {
      "post": {
        "tags": ["Ações"],
        "summary": "Venda de ações",
        "description": "Permite vender uma quantidade específica de ações.",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "cpf": { "type": "string" },
                  "id_investimento": { "type": "string" },
                  "quantidade": { "type": "integer" }
                },
                "required": ["cpf", "id_investimento", "quantidade"]
              }
            }
  
          }
        },
        "responses": {
          "200": {
            "description": "Venda realizada com sucesso.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/analises/mercado/{ticker}": {
      "get": {
        "tags": ["Análises"],
        "summary": "Análise de mercado do ativo",
        "description": "Retorna dados de análise do ativo informado, incluindo preço atual e histórico.",
        "parameters": [
          {
            "name": "ticker",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "Análise retornada.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/analises/carteira/{cpf}": {
      "get": {
        "tags": ["Análises"],
        "summary": "Análise completa da carteira do cliente",
        "parameters": [
          {
            "name": "cpf",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "Análise da carteira retornada.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/calculos/projecao/{cpf}": {
      "get": {
        "tags": ["Análises"],
        "summary": "Projeção de retorno financeiro futuro",
        "parameters": [
          {
            "name": "cpf",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "Projeção retornada.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/analytics/carteira/{cpf}": {
      "get": {
        "tags": ["Analytics"],
        "summary": "Performance completa da carteira",
        "parameters": [
          {
            "name": "cpf",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "Performance calculada.",
            "content": {
              "application/json": { "schema": { "type": "object" } }
            }
          }
        }
      }
    },

    "/graficos/preco/{ticker}": {
      "get": {
        "tags": ["Gráficos"],
        "summary": "Gráfico de evolução de preço",
        "parameters": [
          {
            "name": "ticker",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "Imagem PNG do gráfico.",
            "content": {
              "image/png": {
                "schema": { "type": "string", "format": "binary" }
              }
            }
          }
        }
      }
    },

    "/graficos/projecao/{ticker}": {
      "get": {
        "tags": ["Gráficos"],
        "summary": "Gráfico de projeção de preço (Monte Carlo)",
        "parameters": [
          {
            "name": "ticker",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "Imagem PNG da projeção.",
            "content": {
              "image/png": {
                "schema": { "type": "string", "format": "binary" }
              }
            }
          }
        }
      }
    }

  }
}
       
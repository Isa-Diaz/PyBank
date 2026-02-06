# 📊 Py Invest

Sistema de bancario com gerenciamento e simulação de investimentos baseado em **arquitetura de microserviços**, desenvolvido em **Python** utilizando **Flask**, **FastAPI**, e integração com APIs externas de mercado financeiro.

---

## 🚀 Visão Geral

O **Py Invest** é uma aplicação que permite:

* Gerenciamento de clientes e investidores
* Criação e controle de investimentos
* Consulta de dados financeiros via APIs externas
* Visualização analítica e geração de gráficos
* Interface web para interação com o sistema
* Testes automatizados para validação das funcionalidades

---

## 🏗️ Arquitetura do Projeto

O sistema está organizado em múltiplos microserviços:

```
py_invest/
│
├── client_access_service       → Serviço de acesso e autenticação de clientes
├── investment_gateway_service  → Gateway principal e orquestração dos investimentos
├── investment_data_service     → Serviço de persistência e manipulação dos dados
├── swagger_ui                  → Documentação OpenAPI dos serviços
├── front_end                   → Interface web do sistema
├── test                        → Testes automatizados
└── requirements.txt            → Dependências do projeto
```

---

## 🔧 Tecnologias Utilizadas

* Python
* Flask
* FastAPI
* SQLite / Peewee ORM
* Pandas / NumPy
* Matplotlib
* YFinance (dados financeiros)
* Swagger / OpenAPI
* Pytest (testes automatizados)
* HTML / CSS / JavaScript

---

## ⚙️ Como Executar o Projeto

### ✅ Pré-requisitos

* Python 3.10+
* Pip
* Virtualenv (recomendado)

---

### 📥 Instalação

Clone o repositório:

```bash
git clone https://github.com/Isa-Diaz/PyBank.git
cd PyBank
```


Crie e ative o ambiente virtual:

```bash
python3 -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```
Instale as bibliotecas:

python -m pip install flask-cors

python -m pip install yfinance

python -m pip install matplotlib

python -m pip install seaborn



Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ▶️ Executando os Microserviços

### 📦 Serviço de Dados (Servidor 1)

Responsável pela criação e manutenção das tabelas e persistência dos dados.

```bash
python -m investment_data_service.app
```

Executa em:

```
http://localhost:5000
```

---

### 🔐 Serviço de Acesso de Clientes (Servidor 2)

Responsável pelo cadastro, autenticação e gerenciamento de usuários/clientes na conta corrente.

```bash
python -m client_access_service.controller.controller_access
```

Executa em:

```
http://localhost:5001
```

---

### 🌐 Gateway de Investimentos (Servidor 3)

Responsável pelo cadastro autenticação e gerenciamento de usuários/clientes investidores e seus investimentos.

```bash
python -m investment_gateway_service.app
```

Executa em:

```
http://localhost:5002
```

---

## 🖥️ Interface Web

Os arquivos do frontend estão localizados em:

```
front_end/
```

Para utilizar:

1. cd front_end
python3 -m http.server 5500

2. Abra o arquivo: http://localhost:5500/index.html
 
Navegue pelo sistema via navegador

---

## 📄 Documentação da API

Os arquivos OpenAPI estão disponíveis em:

```
swagger_ui/
```

Eles descrevem os endpoints disponíveis nos microserviços.

---

## 🧪 Testes Automatizados

Para executar os testes:

```bash
pytest
```

Para gerar relatório de cobertura:

```bash
pytest --cov
```

---

## 📊 Funcionalidades Principais

* Cadastro e gerenciamento de clientes
* Controle de investimentos fixos
* Consulta de ativos do mercado financeiro
* Registro de transações
* Análises e gráficos financeiros
* Integração com APIs externas de mercado

---

## 📁 Estrutura Simplificada

```
client_access_service/
├── controller
├── service
└── client

investment_gateway_service/
├── controller_invest
├── service
└── app.py

investment_data_service/
├── controller_storage
├── repository
└── app.py
```

---

## 🧱 Banco de Dados

O sistema cria automaticamente as tabelas necessárias ao iniciar o serviço de dados:

* Usuários
* Investidores
* Tipos de investimentos
* Transações
* Investimentos via API

---

## 📌 Observações

* O projeto utiliza arquitetura modular para facilitar manutenção e escalabilidade.
* Os serviços podem ser executados individualmente.
* A comunicação entre serviços ocorre via HTTP.

---

## 👨‍💻 Autor

Desenvolvido por mim para fins educacionais e experimentação com microserviços e análise financeira em Python.


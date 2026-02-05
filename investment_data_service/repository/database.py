import sqlite3, uuid
import os

def connect():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "database.db")

    conexao = sqlite3.connect(DB_PATH, timeout=5)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao




def create_table_user():
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes(
            id TEXT PRIMARY KEY,
            nome TEXT,
            cpf TEXT NOT NULL UNIQUE CHECK (length(cpf) = 11),
            email TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL UNIQUE CHECK (length(telefone) = 11),
            correntista INTEGER CHECK (correntista IN (0,1)),
            score_credito REAL,
            saldo_cc REAL,
            admin INTEGER CHECK (admin IN (0,1)),
            senha TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()


def create_table_investidor():
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investidor(
            id_cliente TEXT PRIMARY KEY,
            perfil_investidor TEXT,
            patrimonio_total REAL,
            data_cadastro DATE,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)
    conexao.commit()
    conexao.close()
def create_table_tipo_investimento():
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investimentos(
            id_investimento INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id TEXT,
            tipo_investimento TEXT,
            valor_investido REAL,
            data_aplicacao DATE,
            rentabilidade REAL,
            ativo INTEGER CHECK (ativo IN (0,1)),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)
    conexao.commit()
    conexao.close()
def create_table_transacoes():
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes(
            id_transacao INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id TEXT,
            tipo TEXT CHECK (tipo IN ('deposito','saque','transferencia','investimento','ajuste')),
            valor REAL NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            descricao TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)
    conexao.commit()
    conexao.close()
def create_table_investimentos_api():
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investimentos_api(
        id_investimentos INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id TEXT,
            ticker TEXT,
            quantidade REAL,
            preco_unitario REAL,
            custo_total REAL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
                   )
""")
    conexao.commit()
    conexao.close()
def create_table_transacoes_api():
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes_api(
            id_transacao INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id TEXT,
            ticker TEXT,
            tipo TEXT CHECK (tipo IN ('compra', 'venda')),
            quantidade REAL,
            preco_unitario REAL,
            custo_total REAL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )
    """)
    conexao.commit()
    conexao.close()

def insert_user(nome, cpf, email, telefone, correntista, score_credito, saldo_cc, admin,senha):
    conexao = connect()
    cursor = conexao.cursor()

    user_id = str(uuid.uuid4()) 

    cursor.execute(
        """INSERT INTO clientes (id, nome, cpf, email, telefone, correntista, score_credito, saldo_cc, admin,senha)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
           (user_id, nome, cpf, email, telefone, correntista, score_credito, saldo_cc, admin, senha)
    ) 

    conexao.commit()
    conexao.close()
    return user_id
def insert_investidor(id_cliente, perfil_investidor, patrimonio_total, data_cadastro):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute(
        """INSERT INTO investidor (id_cliente, perfil_investidor, patrimonio_total, data_cadastro)
           VALUES (?, ?, ?, ?)""",
        (id_cliente, perfil_investidor, patrimonio_total, data_cadastro)
    )

    conexao.commit()
    conexao.close()
    return id_cliente
def insert_tipo_investimento(id_cliente, tipo_investimento, valor_investido, data_aplicacao, rentabilidade, ativo):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute(
        """INSERT INTO investimentos (cliente_id, tipo_investimento, valor_investido, data_aplicacao, rentabilidade, ativo)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (id_cliente, tipo_investimento, valor_investido, data_aplicacao, rentabilidade, ativo)
    )

    conexao.commit()
    investimento_id = cursor.lastrowid
    conexao.close()

    return investimento_id, id_cliente
def insert_investimento_api(cliente_id, ticker, quantidade, preco_unitario, custo_total):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO investimentos_api (cliente_id, ticker, quantidade, preco_unitario, custo_total)
        VALUES (?, ?, ?, ?, ?)
    """, (cliente_id, ticker, quantidade, preco_unitario, custo_total))
    conexao.commit()
    id_investimento = cursor.lastrowid
    conexao.close()
    return id_investimento
def insert_transacao(cliente_id, tipo, valor, descricao=None):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute(
        """INSERT INTO transacoes (cliente_id, tipo, valor, descricao)
           VALUES (?, ?, ?, ?)""",
        (cliente_id, tipo, valor, descricao)
    )

    conexao.commit()
    transacao_id = cursor.lastrowid
    conexao.close()

    return transacao_id


def listar_investimentos_api(cliente_id):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_investimentos, cliente_id, ticker, quantidade, preco_unitario, custo_total, data
        FROM investimentos_api
        WHERE cliente_id = ?
    """, (cliente_id,))

    linhas = cursor.fetchall()
    conexao.close()
    return linhas
def listar_user():
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes")
    linhas = cursor.fetchall()

    conexao.close()
    return linhas
def listar_investidores():
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM investidor")
    linhas = cursor.fetchall()

    conexao.close()
    return linhas
def listar_investimentos():
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM investimentos")
    linhas = cursor.fetchall()

    conexao.close()
    return linhas
def listar_transacoes(cliente_id):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM transacoes WHERE cliente_id = ? ORDER BY data DESC",
        (cliente_id,)
    )

    linhas = cursor.fetchall()
    conexao.close()
    return linhas


def registrar_operacao_api(cliente_id, ticker, tipo, quantidade, preco_unitario, custo_total):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO transacoes_api (cliente_id, ticker, tipo, quantidade, preco_unitario, custo_total)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cliente_id, ticker, tipo, quantidade, preco_unitario, custo_total))

    conexao.commit()
    conexao.close()


def buscar_cliente_com_investidor(id):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT *
        FROM clientes c
        LEFT JOIN investidor i ON c.id = i.id_cliente
        WHERE c.id = ?
    """, (id,))
    linha = cursor.fetchone()
    conexao.close()
    return linha

def buscar_user_por_id(id):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (id,))
    linha = cursor.fetchone()
    conexao.close()
    return linha

def buscar_investidor_por_id(id):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM investidor WHERE id_cliente = ?", (id,))
    linha = cursor.fetchone()
    conexao.close()
    return linha
def buscar_investimento_por_id(id):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM investimentos WHERE id_investimento = ?", (id,))
    linha = cursor.fetchone()
    conexao.close()
    return linha

def buscar_user_por_cpf(cpf):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes WHERE cpf = ?", (cpf,))
    linha = cursor.fetchone()
    conexao.close()
    return linha

def buscar_user_por_email(email):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes WHERE email = ?", (email,))
    linha = cursor.fetchone()
    conexao.close()
    return linha
def buscar_user_por_telefone(telefone):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes WHERE telefone = ?", (telefone,))
    linha = cursor.fetchone()
    conexao.close()
    return linha
def buscar_investimento_api_por_id(id_investimento):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_investimentos, cliente_id, ticker, quantidade, preco_unitario, custo_total, data
        FROM investimentos_api
        WHERE id_investimentos = ?
    """, (id_investimento,))

    linha = cursor.fetchone()
    conexao.close()
    return linha




def atualizar_user(id, nome=None, cpf=None, email=None, telefone=None,correntista=None, score_credito=None, saldo_cc=None):

    conexao = connect()
    cursor = conexao.cursor()

    campos = []
    valores = []

    if nome is not None:
        campos.append("nome = ?")
        valores.append(nome)

    if cpf is not None:
        campos.append("cpf = ?")
        valores.append(cpf)

    if email is not None:
        campos.append("email = ?")
        valores.append(email)

    if telefone is not None:
        campos.append("telefone = ?")
        valores.append(telefone)

    if correntista is not None:
        campos.append("correntista = ?")
        valores.append(correntista)

    if score_credito is not None:
        campos.append("score_credito = ?")
        valores.append(score_credito)

    if saldo_cc is not None:
        campos.append("saldo_cc = ?")
        valores.append(saldo_cc)

    if not campos:
        return "Nenhum campo enviado para atualizar."

    valores.append(id)

    sql = "UPDATE clientes SET " + ", ".join(campos) + " WHERE id = ?"

    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    return "Usuário atualizado com sucesso!"

def atualizar_investidor(id_cliente, perfil_investidor=None, patrimonio_total=None, data_cadastro=None):
    conexao = connect()
    cursor = conexao.cursor()

    campos = []
    valores = []

    if perfil_investidor is not None:
        campos.append("perfil_investidor = ?")
        valores.append(perfil_investidor)

    if patrimonio_total is not None:
        campos.append("patrimonio_total = ?")
        valores.append(patrimonio_total)

    if data_cadastro is not None:
        campos.append("data_cadastro = ?")
        valores.append(data_cadastro)

    if not campos:
        return "Nenhum campo enviado para atualizar."

    valores.append(id_cliente)

    sql = "UPDATE investidor SET " + ", ".join(campos) + " WHERE id_cliente = ?"

    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    return "Investidor atualizado com sucesso!"

def atualizar_investimento(id_investimento, cliente_id=None, tipo_investimento=None,valor_investido=None, data_aplicacao=None,rentabilidade=None, ativo=None):    
    conexao = connect()
    cursor = conexao.cursor()

    campos = []
    valores = []

    if cliente_id is not None:
        campos.append("cliente_id = ?")
        valores.append(cliente_id)

    if tipo_investimento is not None:
        campos.append("tipo_investimento = ?")
        valores.append(tipo_investimento)

    if valor_investido is not None:
        campos.append("valor_investido = ?")
        valores.append(valor_investido)

    if data_aplicacao is not None:
        campos.append("data_aplicacao = ?")
        valores.append(data_aplicacao)

    if rentabilidade is not None:
        campos.append("rentabilidade = ?")
        valores.append(rentabilidade)

    if ativo is not None:
        campos.append("ativo = ?")
        valores.append(ativo)

    if not campos:
        return "Nenhum campo enviado para atualizar."

    valores.append(id_investimento)

    sql = "UPDATE investimentos SET " + ", ".join(campos) + " WHERE id_investimento = ?"

    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    return "Investimento atualizado com sucesso!"


def atualizar_investimento_api(id_investimento, nova_quantidade, novo_custo_total):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE investimentos_api
        SET quantidade = ?, custo_total = ?
        WHERE id_investimentos = ?
    """, (nova_quantidade, novo_custo_total, id_investimento))

    conexao.commit()
    conexao.close()


def delete_user(id):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()

def delete_investimento(id_investimento):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM investimentos WHERE id_investimento = ?", (id_investimento,))
    conexao.commit()
    conexao.close()

def delete_investimento_api(id_investimento):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM investimentos_api WHERE id_investimentos = ?", (id_investimento,))
    conexao.commit()
    conexao.close()

def buscar_user_por_cpf_e_senha(cpf, senha):
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT * FROM clientes WHERE cpf = ? AND senha = ?",
        (cpf, senha)
    )
    linha = cursor.fetchone()
    conexao.close()
    return linha

def atualizar_senha_por_id(id_cliente, nova_senha):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE clientes SET senha = ? WHERE id = ?",
        (nova_senha, id_cliente)
    )

    conexao.commit()
    conexao.close()

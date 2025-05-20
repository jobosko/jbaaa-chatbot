import sqlite3

DB_PATH = 'db.sqlite3'

def buscar_debito(cpf):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Localizar o condomino pelo CPF
        cursor.execute("SELECT id, nome FROM condomino WHERE cpf = ?", (cpf,))
        resultado = cursor.fetchone()

        if not resultado:
            return None  # CPF não encontrado

        condomino_id, nome = resultado

        # Buscar lançamentos não pagos
        cursor.execute("""
            SELECT valor, vencimento 
            FROM lancamento 
            WHERE condomino_id = ? AND pago = 0
        """, (condomino_id,))
        lancamentos = cursor.fetchall()

        if not lancamentos:
            return {'nome': nome, 'divida': 0.0, 'vencimento': None}

        divida_total = sum(l[0] for l in lancamentos)
        vencimento_proximo = min(l[1] for l in lancamentos if l[1])

        return {
            'nome': nome,
            'divida': divida_total,
            'vencimento': vencimento_proximo
        }

    finally:
        conn.close()
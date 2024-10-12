import psycopg2
import os

def criar_conexao():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DATABASE"),
        sslmode="require"  # Esse valor é passado diretamente, como no seu URL
    )

def fechar_conexao(conexao):
    if conexao:
        conexao.close()



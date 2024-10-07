import mysql.connector

def criar_conexao():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "1234",
        database = "VozUrbana"
    )

def fechar_conexao(conexao):
    if conexao:
        conexao.close()
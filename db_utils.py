import pymysql.cursors
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME  # Importando as variáveis de configuração

# Função de conexão ao banco de dados
def connect_db():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor  # Usando DictCursor para resultados como dicionário
    )
    return connection

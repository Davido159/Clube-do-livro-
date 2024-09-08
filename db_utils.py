# db_utils.py
from mysql.connector import connect
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def connect_db():
    return connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

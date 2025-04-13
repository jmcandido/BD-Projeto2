
# db.py
import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',      # atualize conforme sua configuração
            user='YOUR_USER',      # seu usuário MySQL
            password='YOUR_PASSWORD',  # sua senha
            database='sales_db'    # nome do seu banco de dados
        )
        return connection
    except Error as e:
        print("Erro ao conectar com o MySQL:", e)
        return None

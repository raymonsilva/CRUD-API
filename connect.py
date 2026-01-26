import psycopg2 as pg
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()

def conn():
    try:
        pwd = os.getenv("DB_PASSWORD")
        conecta = pg.connect(

            user="postgres",
            password= pwd,
            host="localhost",
            port=5431,
            database="viagens"
            )

        print("Conectado com sucesso")

        return conecta

    except Error as e:
        print("Erro ao conectar ao banco de dados", e)

        
def encerrar_conexao(conecta):
    if conecta:
        conecta.close()
        print("Conexao encerrada")
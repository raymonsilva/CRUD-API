from connect import conn, encerrar_conexao
from Generic_DAO import *
from flask import jsonify

def list_destinos():
    connection = conn()
    data = get_data(connection, "destinos")
    encerrar_conexao(connection)
    return jsonify(data)
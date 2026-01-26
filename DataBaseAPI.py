from flask import jsonify, request
from connect import conn, encerrar_conexao
from psycopg2 import sql
from flask import Flask
from Generic_DAO import *
from Services.Usuarios_Services import *
from Services.Reservas_Service import *
from Services.Destinos_Service import *

# DataBaseAPI - API for database operations using Flask
# Get data from postgresql database and return as JSON

app = Flask(__name__)
app.json.sort_keys = False

# API Routes
@app.route('/list_tables')
def list_tables():
    connection = conn()
    tables = get_tables(connection)
    return jsonify(tables)
    encerrar_conexao(connection)

@app.route('/list_columns/<table_name>')
def list_columns(table_name):
    connection = conn()
    columns = get_columns(connection, table_name)
    return jsonify(columns)
    encerrar_conexao(connection)

@app.route('/list_usuarios')
def route_list_usuarios():
    return list_users()

@app.route('/list_reservas')
def route_list_reservas():
    return list_reservas()

@app.route('/list_destinos')
def route_list_destinos():
    return list_destinos()

@app.route('/post_data/<table_name>', methods=['POST'])
def post_data(table_name):
    connection = conn()
    return create_register(connection, table_name, request.json)

@app.route('/update_data/<table_name>', methods=['PUT'])
def update_data(table_name):
    connection = conn()
    return update_register(connection, table_name, request.json)

@app.route('/delete_data/<table_name>/<id_val>', methods=['DELETE'])
def delete_data(table_name, id_val):
    connection = conn()
    return delete_register(connection, table_name, id_val)


if __name__ == "__main__":
    app.run(debug=True)
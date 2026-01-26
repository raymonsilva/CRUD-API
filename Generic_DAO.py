from connect import conn, encerrar_conexao
import psycopg2.sql as sql
from flask import jsonify


# Get Tables From Database
def get_tables(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        return [row[0] for row in cursor.fetchall()]

# Get Columns From Table
def get_columns(connection, table_name):
    with connection.cursor() as cursor:
        query = sql.SQL("SELECT * FROM {} LIMIT 0").format(sql.Identifier(table_name))
        cursor.execute(query)
        return [desc[0] for desc in cursor.description]


def get_data(connection, table_name):
    with connection.cursor() as cursor:
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        cursor.execute(query)
        
        columns = [desc[0] for desc in cursor.description]
        results = []

        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results

# Create Register From Table
def create_register(connection, table_name, data=None):
    if data:
        cursor = connection.cursor()
        columns = get_columns(connection, table_name)
        if 'id' in columns:
            columns.remove('id')
        values = [data[col] for col in columns]

        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        cursor.execute(insert_query, values)
        connection.commit()
        encerrar_conexao(connection)
        return jsonify({"message": "Registro criado com sucesso"}), 201
    else:
        return jsonify({"error": "Dados inválidos"}), 406


# Update Register From Table
def update_register(connection, table_name, data=None):
    if data:
        cursor = connection.cursor()
        columns = get_columns(connection, table_name)
        if 'id' in columns:
            columns.remove('id')
        
        id_val = data.get("id")
        
        # Filter values to match columns (exclude id if present in data values)
        # Assuming data keys match columns, or at least values are in order of columns
        # To be safe, we reconstruct values based on columns order:
        values = [data[col] for col in columns]

        assignments = [sql.SQL("{} = {}").format(sql.Identifier(col), sql.Placeholder()) for col in columns]

        update_query = sql.SQL("UPDATE {} SET {} WHERE id = {}").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(assignments),
            sql.Placeholder()
        )
        cursor.execute(update_query, values + [id_val])
        connection.commit()
        encerrar_conexao(connection)
        return jsonify({"message": "Registro atualizado com sucesso"}), 201
    else:
        return jsonify({"error": "Dados inválidos"}), 406

# Delete Register From Table
def delete_register(connection, table_name, id_val=None):
   if id_val:
        cursor = connection.cursor()
        delete_query = sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(table_name))
        cursor.execute(delete_query, (id_val,))
        connection.commit()
        encerrar_conexao(connection)
        return jsonify({"message": "Registro deletado com sucesso"}), 201
   else:
        return jsonify({"error": "Dados inválidos"}), 406
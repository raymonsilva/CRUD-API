from flask import jsonify
from connect import conn
from Generic_DAO import *

def list_users():
    connection = conn()
    users = get_data(connection, "usuarios")
    for user in users:
        if user.get("data_nascimento"):
            user["data_nascimento"] = user["data_nascimento"].strftime("%Y-%m-%d")
    return jsonify(users)
    
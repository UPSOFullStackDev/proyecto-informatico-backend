from flask import request, jsonify
from extensions import mysql, app
from api.models.data_models import Client, SimpleBill
from utils.decorators import token_required, user_resource
from utils.helpers import validate_data

@app.route("/user/<int:user_id>/clients", methods=["GET"])
@token_required
@user_resource
def get_clients_list(user_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute("SELECT * FROM Client WHERE User_idUser = {0}".format(user_id))
    data = cur.fetchall()

    # Convert Rows
    clientsList = []
    for row in data:
        objClient = Client(row)
        clientsList.append(objClient.to_json())

    # Return List
    return jsonify(clientsList)

@app.route("/user/<int:user_id>/clients", methods=["POST"])
@token_required
@user_resource
def add_client(user_id):
    # Set requirements and get data
    data = request.get_json()
    required = ["name", "surname", "address", "email"]

    # Check if all the values where sended and are not empty
    valid, error = validate_data(data, required)
    if not valid:
        return jsonify({"message": error}), 400

    # Get data from POST request
    name = data["name"]
    surname = data["surname"]
    address = data["address"]
    email = data["email"]

    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f'INSERT INTO Client (name, surname, address, email, User_idUser) VALUES ("{name}", "{surname}", "{address}", "{email}", {user_id})')

    # Save Changes in the DB
    mysql.connection.commit()

    # Get the last inserted ID
    cur.execute("SELECT LAST_INSERT_ID()")
    new_id = cur.fetchone()
    new_id = new_id[0]

    # Return the added client
    return jsonify({
        "id": new_id,
        "name": name,
        "surname": surname,
        "address": address,
        "email": email,
        "user_id": user_id
    })

@app.route("/user/<int:user_id>/clients/<int:client_id>", methods=["GET"])
@token_required
@user_resource
def get_client(user_id, client_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f"SELECT * FROM Client WHERE idClient = {client_id} AND User_idUser = {user_id}")
    data = cur.fetchone()

    # Check if Client Exist
    if not data:
        return jsonify({"message": "Client not found!"}), 404

    # Convert Row into Object
    objClient = Client(data)

    # Return Client
    return jsonify(objClient.to_json())

@app.route("/user/<int:user_id>/clients/<int:client_id>", methods=["DELETE"])
@token_required
@user_resource
def delete_client(user_id, client_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f"DELETE FROM Client WHERE idClient = {client_id} AND User_idUser = {user_id}")

    # Save Changes in the DB
    mysql.connection.commit()

    # Return Confirmation Message
    return jsonify({"message": "Deleted", "id": client_id})

@app.route("/user/<int:user_id>/clients/<int:client_id>", methods=["PUT"])
@token_required
@user_resource
def modify_client(user_id, client_id):
    # Set requirements and get data
    data = request.get_json()
    required = ["name", "surname", "address", "email"]

    # Check if all the values where sended and are not empty
    valid, error = validate_data(data, required)
    if not valid:
        return jsonify({"message": error}), 400

    # Get data from POST request
    name = data["name"]
    surname = data["surname"]
    address = data["address"]
    email = data["email"]

    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f'UPDATE Client SET name = "{name}", surname = "{surname}", address = "{address}", email = "{email}" WHERE idClient = {client_id} AND User_idUser = {user_id}')

    # Save Changes in the DB
    mysql.connection.commit()

    # Return Updated Client
    return jsonify({
        "id": client_id,
        "name": name,
        "surname": surname,
        "address": address,
        "email": email,
        "user_id": user_id
    })

@app.route("/user/<int:user_id>/clients/<int:client_id>/bills", methods=["GET"])
@token_required
@user_resource
def get_client_bills(user_id, client_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f"SELECT * FROM Bill WHERE Client_idClient = {client_id} AND User_idUser = {user_id}")
    data = cur.fetchall()

    # Check if client has products
    if not data:
        return jsonify({"message": "Client has no bills"}), 404

    # Convert Rows
    billList = []
    for row in data:
        objBill = SimpleBill(row)
        billList.append(objBill.to_json())

    # Return bills
    return jsonify(billList)
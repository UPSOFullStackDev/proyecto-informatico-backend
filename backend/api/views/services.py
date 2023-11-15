from flask import request, jsonify
from extensions import mysql, app
from api.models.data_models import Service
from utils.decorators import token_required, user_resource
from utils.helpers import validate_data

@app.route("/user/<int:user_id>/services", methods=["GET"])
@token_required
@user_resource
def get_services_list(user_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute("SELECT * FROM Service WHERE User_idUser = {0}".format(user_id))
    data = cur.fetchall()

    # Convert Rows
    ServicesList = []
    for row in data:
        objService = Service(row)
        ServicesList.append(objService.to_json())

    # Return List
    return  jsonify(ServicesList)

@app.route("/user/<int:user_id>/services", methods = ["POST"])
@token_required
@user_resource
def add_service(user_id):
    # Set requirements and get data
    data = request.get_json()
    required = ["name", "description", "price"]

    # Check if all the values where sended and are not empty
    valid, error = validate_data(data, required)
    if not valid:
        return jsonify({"message": error}), 400

    # Get data from POST request
    name = data["name"]
    description = data["description"]
    price = data["price"]

    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    try:
        cur.execute(f'INSERT INTO Service (name, description, price, User_idUser) VALUES ("{name}","{description}", {price}, {user_id})')

    # Catch Errors
    except:
        return jsonify({"message" : "Error inserting data in the DataBase, check your values!"}), 400

    # Save Changes in the DB
    mysql.connection.commit()

    # Get the last inserted ID
    cur.execute("SELECT LAST_INSERT_ID()")
    new_id = cur.fetchone()
    new_id = new_id[0]

    # Return the added service
    return jsonify({
        "id" : new_id,
        "name" : name,
        "description" : description,
        "price" : price,
        "user_id" : user_id
        })

@app.route("/user/<int:user_id>/services/<int:service_id>", methods = ["GET"])
@token_required
@user_resource
def get_service(user_id, service_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f"SELECT * FROM Service WHERE idService = {service_id} AND User_idUser = {user_id}")
    data = cur.fetchone()

    # Check if Service Exist
    if not data:
        return jsonify({"message" : "Service not found!"}), 404

    # Convert Row into Object
    objService = Service(data)

    # Return Service
    return  jsonify(objService.to_json())

@app.route("/user/<int:user_id>/services/<int:service_id>", methods = ["DELETE"])
@token_required
@user_resource
def delete_service(user_id, service_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f"DELETE FROM Service WHERE idService = {service_id} AND User_idUser = {user_id}")

    # Save Changes in the DB
    mysql.connection.commit()

    # Return Confirmation Message
    return jsonify({"message" : "Deleted", "id" : service_id})

@app.route("/user/<int:user_id>/services/<int:service_id>", methods = ["PUT"])
@token_required
@user_resource
def modify_service(user_id, service_id):
    # Set requirements and get data
    data = request.get_json()
    required = ["name", "description", "price"]

    # Check if all the values where sended and are not empty
    valid, error = validate_data(data, required)
    if not valid:
        return jsonify({"message": error}), 400

    # Get data from POST request
    name = data["name"]
    description = data["description"]
    price = data["price"]

    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    try:
        cur.execute(f'UPDATE Service SET name = "{name}", description = "{description}", price = {price} WHERE idService = {service_id} AND User_idUser = {user_id}')

    # Catch Errors
    except:
        return jsonify({"message" : "Error inserting data in the DataBase, check your values!"}), 400

    # Save Changes in the DB
    mysql.connection.commit()

    # Return Updated Service
    return jsonify({
        "id" : service_id,
        "name" : name,
        "description" : description,
        "price" : price,
        "user_id" : user_id
        })

"""
Consejo Adicional: Considera usar parámetros de consulta en lugar de rutas para filtrar resultados, 
especialmente si planeas agregar más filtros en el futuro. Por ejemplo, en lugar de /user/<user_id>/services, 
podrías tener /services?user_id=<user_id>. Sin embargo, esto es más una preferencia y depende del diseño general 
de tu API.
"""

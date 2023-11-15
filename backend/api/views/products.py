from flask import request, jsonify
from extensions import mysql, app
from api.models.data_models import Product
from utils.decorators import token_required, user_resource
from utils.helpers import validate_data

@app.route("/user/<int:user_id>/products", methods=["GET"])
@token_required
@user_resource
def get_products_list(user_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute("SELECT * FROM Product WHERE User_idUser = {0}".format(user_id))
    data = cur.fetchall()

    # Convert Rows
    productsList = []
    for row in data:
        objProduct = Product(row)
        productsList.append(objProduct.to_json())

    # Return List
    return  jsonify(productsList)

@app.route("/user/<int:user_id>/products", methods = ["POST"])
@token_required
@user_resource
def add_product(user_id):
    # Set requirements and get data
    data = request.get_json()
    required = ["name", "description", "price", "stock"]

    # Check if all the values where sended and are not empty
    valid, error = validate_data(data, required)
    if not valid:
        return jsonify({"message": error}), 400

    # Get data from POST request
    name = data["name"]
    description = data["description"]
    price = data["price"]
    stock = data["stock"]

    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    try:
        cur.execute(f'INSERT INTO Product (name, description, price, stock, User_idUser) VALUES ("{name}","{description}", {price}, {stock}, {user_id})')

    # Catch Errors
    except:
        return jsonify({"message" : "Error inserting data in the DataBase, check your values!"}), 400

    # Save Changes in the DB
    mysql.connection.commit()

    # Get the last inserted ID
    cur.execute("SELECT LAST_INSERT_ID()")
    new_id = cur.fetchone()
    new_id = new_id[0]

    # Return the added product
    return jsonify({
        "id" : new_id,
        "name" : name,
        "description" : description,
        "price" : price,
        "stock" : stock,
        "user_id" : user_id
        })

@app.route("/user/<int:user_id>/products/<int:product_id>", methods = ["GET"])
@token_required
@user_resource
def get_product(user_id, product_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f"SELECT * FROM Product WHERE idProduct = {product_id} AND User_idUser = {user_id}")
    data = cur.fetchone()

    # Check if Product Exist
    if not data:
        return jsonify({"message" : "Product not found!"}), 404

    # Convert Row into Object
    objProduct = Product(data)

    # Return Product
    return  jsonify(objProduct.to_json())

@app.route("/user/<int:user_id>/products/<int:product_id>", methods = ["DELETE"])
@token_required
@user_resource
def delete_product(user_id, product_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f"DELETE FROM Product WHERE idProduct = {product_id} AND User_idUser = {user_id}")

    # Save Changes in the DB
    mysql.connection.commit()

    # Return Confirmation Message
    return jsonify({"message" : "Deleted", "id" : product_id})

@app.route("/user/<int:user_id>/products/<int:product_id>", methods = ["PUT"])
@token_required
@user_resource
def modify_product(user_id, product_id):
    # Set requirements and get data
    data = request.get_json()
    required = ["name", "description", "price", "stock"]

    # Check if all the values where sended and are not empty
    valid, error = validate_data(data, required)
    if not valid:
        return jsonify({"message": error}), 400

    # Get data from POST request
    name = data["name"]
    description = data["description"]
    price = data["price"]
    stock = data["stock"]

    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    try:
        cur.execute(f'UPDATE Product SET name = "{name}", description = "{description}", price = {price}, stock = {stock} WHERE idProduct = {product_id} AND User_idUser = {user_id}')

    # Catch Errors
    except:
        return jsonify({"message" : "Error inserting data in the DataBase, check your values!"}), 400

    # Save Changes in the DB
    mysql.connection.commit()

    # Return Updated Product
    return jsonify({
        "id" : product_id,
        "name" : name,
        "description" : description,
        "price" : price,
        "stock" : stock,
        "user_id" : user_id
        })
import jwt, datetime
from flask import request, jsonify
from extensions import mysql, app
from utils.helpers  import encode_password, validate_data
from utils.decorators import token_required, user_resource
from api.models.data_models import User

@app.route('/user/register', methods=["POST"])
def register_user():
    # Set requirements and get data
    data = request.get_json()
    required = ["name", "username", "password", "email"]

    # Check if all the values where sended and are not empty
    valid, error = validate_data(data, required)
    if not valid:
        return jsonify({"message": error}), 400

    # Get data from POST request
    name = data["name"]
    username = data["username"]
    password = data["password"]
    email = data["email"]

    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f'SELECT * FROM User WHERE email = "{email}"')
    data = cur.fetchall()

    # Check if email already exist
    if data:
        return jsonify({"message" : "Already registered email!"}), 409

    # Encode Password
    encoded_password = encode_password(password, app.config["SECRET_KEY"])

    # SQL Query
    cur.execute(f'INSERT INTO User (name, username, password, email) VALUES ("{name}","{username}", "{encoded_password}", "{email}")')

    # Save Changes in the DB
    mysql.connection.commit()

    # Get the last inserted ID
    cur.execute("SELECT LAST_INSERT_ID()")
    new_id = cur.fetchone()
    new_id = new_id[0]

    # Return the added user
    return jsonify({
        "id" : new_id,
        "name" : name,
        "username" : username,
        "email" : email
        })

@app.route('/user/login', methods=['POST'])
def login():
    # Extract data from Log In
    auth = request.authorization

    # Check if data is provided
    if not auth or not auth.username or not auth.password:
        return jsonify({"message" : "Not autorized!"}), 401

    # Encode Password
    password = encode_password(auth.password, app.config["SECRET_KEY"])

    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f'SELECT * FROM User WHERE email = "{auth.username}" AND password = "{password}"')
    row = cur.fetchone()

    # Check if data is correct
    if not row:
        return jsonify({"message" : "Not autorized!"}), 401

    # User Exist and match in the DB
    token = jwt.encode({
        "id" : row[0],
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes = 100)
    }, app.config["SECRET_KEY"])


    return jsonify({"token" : token, "username" : row[2], "id" : row[0]})

@app.route('/user/<int:user_id>', methods=['GET'])
@token_required
@user_resource
def get_user(user_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f'SELECT * FROM User WHERE idUser = {user_id}')
    data = cur.fetchone()

    # Check if data is correct
    if not data:
        return jsonify({"message" : "User not found!"}), 404

    # Convert Row into Object
    objUser = User(data)

    # Return User
    return jsonify(objUser.to_json())
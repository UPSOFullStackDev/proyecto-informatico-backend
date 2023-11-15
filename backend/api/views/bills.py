import datetime
from flask import request, jsonify
from extensions import mysql, app
from api.models.data_models import FullBill, SimpleBill, Client
from utils.decorators import token_required, user_resource
from utils.helpers import validate_data

@app.route("/user/<int:user_id>/sales", methods=["GET"])
@token_required
@user_resource
def get_sales(user_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute("SELECT Bill.*, CONCAT(Client.name, ' ', Client.surname) AS client_name FROM Bill INNER JOIN Client ON Bill.Client_idClient = Client.idClient WHERE Bill.User_idUser = {0} ORDER BY Bill.date DESC;".format(user_id))
    data = cur.fetchall()


    # Convert Rows
    billList = []
    for row in data:
        objProduct = SimpleBill(row)
        billList.append(objProduct.to_json())

    # Return List
    return  jsonify(billList)

@app.route("/user/<int:user_id>/sales", methods=["POST"])
@token_required
@user_resource
def add_sale(user_id):
    # Set requirements and get data
    data = request.get_json()
    required = ["client_id", "products", "services"]

    # Check if all the values where sended and are not empty
    valid, error = validate_data(data, required)
    if not valid:
        return jsonify({"message": error}), 400

    # Extra validations, (check if types are correct)
    if not (isinstance(data["client_id"], int) and isinstance(data["products"], list) and isinstance(data["services"], list)):
        return jsonify({"message": "Invalid format, expected client_id:int, products:list, services:list !"}), 400
    # Extra validations, (check one of the list contains sth)
    if len(data["products"]) == 0 and len(data["services"]) == 0:
        return jsonify({"message": "Cannot accept two empty lists!"}), 400

    # Get data from POST request
    client_id = data["client_id"]
    products = data["products"]
    services = data["services"]

    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Querys
    try:
        cur.execute(f"SELECT * FROM Client WHERE idClient IN ({client_id}) AND User_idUser = {user_id}")
        data = cur.fetchone()

        # If client not found
        if not data:
            return jsonify({"message" : f"Check your client ID, client with id: {client_id} wasn't found!"}), 404

        client = Client(data).to_json()

        # Calculate the final price
        price = 0

        # If there is more than 0 services in the list
        serviceList = []
        if len(services) > 0:
            # Transform list to str
            services_formatted = ",".join(map(str, services))

            # Consult services with given ids
            cur.execute(f"SELECT idService, price, name FROM Service WHERE idService IN ({services_formatted}) AND User_idUser = {user_id}")
            data = cur.fetchall()
            data_list = [list(tuplee) for tuplee in data]

            # Check if all services exist / belong to user
            for id_service in services:
                found = False
                for row in data_list:
                    if id_service == row[0]:
                        # Add service, price
                        serviceList.append({
                            "service_id" : row[0],
                            "name" : row[2],
                            "price" : row[1]
                            })
                        price += row[1]
                        found = True
                        break

                if not found:
                    return jsonify({"message" : f"Service with id {id_service} not found!"}), 400

        # If there is more than 0 products in the list
        productList = []
        if len(products) > 0:
            # Transform list to str
            products_formatted = ",".join(map(str, products))

            # Consult products with given ids
            cur.execute(f"SELECT idProduct, price, name, stock FROM Product WHERE idProduct IN ({products_formatted}) AND User_idUser = {user_id}")
            data = cur.fetchall()
            data_list = [list(tuplee) for tuplee in data]

            # Check if all products exist / belong to user
            for id_product in products:
                found = False
                for row in data_list:
                    if id_product == row[0]:

                        # Check for stock
                        if row[3] <= 0:
                                return jsonify({"message" : f"Check your product IDs, product with id: {id_product} is out of stock!"}), 400

                        # Add product, price and minus stock
                        productList.append({
                            "product_id" : row[0],
                            "name" : row[2],
                            "price" : row[1]
                            })
                        price += row[1]
                        row[3] -= 1
                        found = True
                        break

                if not found:
                    return jsonify({"message" : f"Product with id {id_product} not found!"}), 400

            # Update Stock
            for product in data_list:
                cur.execute(f"UPDATE Product SET stock = {product[3]} WHERE idProduct = {product[0]}")

        # Create the bill
        date = datetime.datetime.now()
        cur.execute(f'INSERT INTO Bill (Client_idClient, price, date, User_idUser) VALUES ({client_id}, {price}, "{date}", {user_id})')

        # Get the last inserted ID
        cur.execute("SELECT LAST_INSERT_ID()")
        bill_id = cur.fetchone()
        bill_id = bill_id[0]

        # Add Products to table bill has product
        if products:
            query = f"INSERT INTO Bill_has_Product (Bill_idBill, Product_idProduct) VALUES "
            values = ', '.join([f"({bill_id}, {product_id})" for product_id in products])
            query += values
            cur.execute(query)

        # Add Services to table bill has service
        if services:
            query = f"INSERT INTO Bill_has_Service (Bill_idBill, Service_idService) VALUES "
            values = ', '.join([f"({bill_id}, {service_id})" for service_id in services])
            query += values
            cur.execute(query)

    # Catch Errors
    except Exception as Error:
        return jsonify({"message" : f"Error inserting data in the DataBase, check your values! error: {Error}"}), 400

    # Save Changes in the DB
    mysql.connection.commit()

    # Return new Bill
    return jsonify({
        "id" : bill_id,
        "client" : client,
        "price" : price,
        "date" : date,
        "products" : productList,
        "services" : serviceList,
        "user_id" : user_id
    })

@app.route("/user/<int:user_id>/sales/<int:bill_id>", methods=["GET"])
@token_required
@user_resource
def get_sale(user_id, bill_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute(f"SELECT * FROM Bill WHERE idBill = {bill_id} AND User_idUser = {user_id}")
    data = cur.fetchone()

    # Check if Service Exist
    if not data:
        return jsonify({"message" : "Bill not found!"}), 404

    # Convert Row into Object
    objBill = FullBill(data)

    # Get the client and Add client data to bill
    cur.execute(f"SELECT * FROM Client WHERE idClient = {objBill.get_client_id()} AND User_idUser = {user_id}")
    data = cur.fetchone()
    objClient = Client(data)
    objBill.set_client(objClient.to_json())

    # Search for products and add to bill
    cur.execute(f"SELECT Product.idProduct, Product.name, Product.price FROM Bill_has_Product JOIN Product ON Bill_has_Product.Product_idProduct = Product.idProduct WHERE Bill_has_Product.Bill_idBill = {bill_id}")
    data = cur.fetchall()
    objBill.set_product(data)

    # Search for products and add to bill
    cur.execute(f"SELECT Service.idService, Service.name, Service.price FROM Bill_has_Service JOIN Service ON Bill_has_Service.Service_idService = Service.idService WHERE Bill_has_Service.Bill_idBill = {bill_id}")
    data = cur.fetchall()
    objBill.set_service(data)

    # Return Bill
    return  jsonify(objBill.to_json())

@app.route("/user/<int:user_id>/sales/clients", methods=["GET"])
@token_required
@user_resource
def get_clients_sales(user_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute("SELECT c.idClient, c.name, SUM(b.price) AS totalSpent, COUNT(b.idBill) AS billCount FROM Bill AS b JOIN Client AS c ON b.Client_idClient = c.idClient WHERE b.User_idUser = {0} GROUP BY c.idClient, c.name ORDER BY totalSpent DESC;".format(user_id))
    data = cur.fetchall()

    # Check if bills where found
    if not data:
        return jsonify({"message" : "0 Bills Found!"}), 404

    # Format rows and append to a list
    clientSalesList = []
    for clientRow in data:
        info = {
            "client_id" : clientRow[0],
            "name" : clientRow[1],
            "spent_sum" : clientRow[2],
            "bill_count" : clientRow[3]
        }
        clientSalesList.append(info)

    # Return List
    return  jsonify(clientSalesList)

@app.route("/user/<int:user_id>/sales/products", methods=["GET"])
@token_required
@user_resource
def get_products_sales(user_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute("SELECT p.idProduct AS product_id, p.name AS product_name, COUNT(bhp.Product_idProduct) AS sold_count, SUM(p.price) AS sold_sum FROM Product p JOIN Bill_has_Product bhp ON p.idProduct = bhp.Product_idProduct WHERE p.User_idUser = {0} GROUP BY p.idProduct, p.name ORDER BY sold_sum DESC;".format(user_id))
    data = cur.fetchall()

    # Check if products where found
    if not data:
        return jsonify({"message" : "Products not found!"}), 404

    # Format rows and append to a list
    productSalesList = []
    for clientRow in data:
        info = {
            "product_id" : clientRow[0],
            "name" : clientRow[1],
            "sold_count" : clientRow[2],
            "sold_sum" : clientRow[3]
        }
        productSalesList.append(info)

    # Return List
    return  jsonify(productSalesList)

@app.route("/user/<int:user_id>/sales/services", methods=["GET"])
@token_required
@user_resource
def get_services_sales(user_id):
    # Connect to the DataBase
    cur = mysql.connection.cursor()

    # SQL Query
    cur.execute("SELECT p.idService AS product_id, p.name AS product_name, COUNT(bhp.Service_idService) AS sold_count, SUM(p.price) AS sold_sum FROM Service p JOIN Bill_has_Service bhp ON p.idService = bhp.Service_idService WHERE p.User_idUser = {0} GROUP BY p.idService, p.name ORDER BY sold_sum DESC;".format(user_id))
    data = cur.fetchall()

    # Check if services where found
    if not data:
        return jsonify({"message" : "Services not found!"}), 404

    # Format rows and append to a list
    serviceSalesList = []
    for clientRow in data:
        info = {
            "service_id" : clientRow[0],
            "name" : clientRow[1],
            "sold_count" : clientRow[2],
            "sold_sum" : clientRow[3]
        }
        serviceSalesList.append(info)

    # Return List
    return  jsonify(serviceSalesList)

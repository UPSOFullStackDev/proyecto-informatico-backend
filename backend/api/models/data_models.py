# Métodos 'to_json': Considerar usar una biblioteca como Marshmallow para serializar y deserializar objetos.
# proporciona una forma más estructurada y escalable de manejar la serialización y deserialización de tus objetos.

class Client():
    """Representa un cliente en la base de datos."""
    def __init__(self, row):
        self.__id = row[0]
        self.__name = row[1]
        self.__surname = row[2]
        self.__address = row[3]
        self.__email = row[4]
        self.__user_id = row[5]

    def to_json(self):
        """Devuelve una representación JSON del objeto."""
        return {
            "id" : self.__id,
            "name" : self.__name,
            "surname" : self.__surname,
            "address" : self.__address,
            "email" : self.__email,
            "user_id" : self.__user_id,
        }


class Product():
    """Representa un producto en la base de datos."""
    def __init__(self, row):
        self.__id = row[0]
        self.__name = row[1]
        self.__stock = row[2]
        self.__description = row[3]
        self.__price = row[4]
        self.__user_id = row[5]

    def get_stock(self):
        return self.__stock

    def get_price(self):
        return self.__price

    def to_json(self):
        """Devuelve una representación JSON del objeto."""
        return {
            "id" : self.__id,
            "name" : self.__name,
            "description" : self.__description,
            "price" : self.__price,
            "stock" : self.__stock,
            "user_id" : self.__user_id,
        }

class Service():
    """Representa un servicio en la base de datos."""
    def __init__(self, row):
        self.__id = row[0]
        self.__price = row[1]
        self.__name = row[2]
        self.__description = row[3]
        self.__user_id = row[4]

    def get_price(self):
        return self.__price

    def to_json(self):
        """Devuelve una representación JSON del objeto."""
        return {
            "id" : self.__id,
            "name" : self.__name,
            "description" : self.__description,
            "price" : self.__price,
            "user_id" : self.__user_id,
        }

class SimpleBill():
    """Representa una factura en la base de datos. Incluye unicamente id de cliente, precio y fecha"""
    def __init__(self, row):
        self.__id = row[0]
        self.__client_id = row[1]
        self.__price = row[2]
        self.__date = row[3]
        self.__user_id = row[4]

        # Check if full name is included
        if len(row) > 5:
            self.__full_name = row[5]
        else:
            self.__full_name = None

    def to_json(self):
        bill_json = {
            "id" : self.__id,
            "client_id" : self.__client_id,
            "date" : self.__date,
            "price" : self.__price,
            "user_id" : self.__user_id
        }

        # Check if full name is included
        if self.__full_name is not None:
            # Add full name to the json
            bill_json["full_name"] = self.__full_name

        return bill_json

class FullBill():
    """Representa una factura en la base de datos. Incluye datos del cliente, productos y servicios a detalle"""
    def __init__(self, row):
        self.__id = row[0]
        self.__client_id = row[1]
        self.__price = row[2]
        self.__date = row[3]
        self.__user_id = row[4]
        self.__products = []
        self.__services = []
        self.__client = ""

    def set_product(self, productList):
        for product in productList:
            id = product[0]
            name = product[1]
            price = product[2]
            self.__products.append({
                "product_id" : id,
                "name" : name,
                "price" : price
            })

    def set_service(self, serviceList):
        for service in serviceList:
            id = service[0]
            name = service[1]
            price = service[2]
            self.__services.append({
                "service_id" : id,
                "name" : name,
                "price" : price
            })

    def set_client(self, client):
        self.__client = client

    def get_client_id(self):
        return self.__client_id

    def to_json(self):
        """Devuelve una representación JSON del objeto."""
        return {
            "id" : self.__id,
            "client_id" : self.__client_id,
            "client" : self.__client,
            "date" : self.__date,
            "price" : self.__price,
            "products": self.__products,
            "services": self.__services,
            "user_id" : self.__user_id
        }

class User():
    """Representa un usuario en la base de datos."""
    def __init__(self, row):
        self.__id = row[0]
        self.__name = row[1]
        self.__username = row[2]
        self.__email = row[4]

    def to_json(self):
        """Devuelve una representación JSON del objeto."""
        return {
            "id" : self.__id,
            "name" : self.__name,
            "username" : self.__username,
            "email" : self.__email
        }

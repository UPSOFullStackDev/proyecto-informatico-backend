from flask import Flask
from flask_mysqldb import MySQL
from extensions import mysql
from config.settings import Config
from api.views.auth import *
from api.views.products import *
from api.views.services import *
from api.views.bills import *
from api.views.clients import *
from utils.helpers import encode_password, validate_data
from utils.decorators import token_required, user_resource
from extensions import app

if __name__ == "__main__":
    app.run(debug = True, port = 5000)
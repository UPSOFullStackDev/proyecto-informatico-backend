from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from config.settings import Config

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)
CORS(app)
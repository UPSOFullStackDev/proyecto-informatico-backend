from decouple import config

class Config:
    # Configuración de MySQL
    MYSQL_HOST = config('MYSQL_HOST')
    MYSQL_USER = config('MYSQL_USER')
    MYSQL_PASSWORD = config('MYSQL_PASSWORD')
    MYSQL_DB = config('MYSQL_DB')

    # Clave secreta
    SECRET_KEY = config('SECRET_KEY')

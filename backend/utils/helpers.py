# Utilidades
import hashlib, base64

def encode_password(password, seed):
    """
    Codifica la contraseña utilizando PBKDF2 y SHA256.
    
    Args:
    - password (str): Contraseña a codificar.
    - seed (str): Semilla para la codificación.
    
    Returns:
    - str: Contraseña codificada en base64.
    """
    b_seed = seed.encode('utf-8')
    b_password = password.encode('utf-8')
    encoded_password = hashlib.pbkdf2_hmac('sha256', b_password, b_seed, 100000)
    encoded_password_b64 = base64.b64encode(encoded_password).decode('utf-8')
    return encoded_password_b64

# def validate_data(data,required):
#     # Check if all the values where sended and are not empty
#     for field in required:

#         # Check if field exist
#         if field not in data:
#             return False, f"Missing '{field}' in the JSON!"

#         # Check if str field is not empty
#         if isinstance(data[field], str) and data[field] == "":
#             return False, f"The attribute '{field}' cannot be empty!"

#         # Check if int/float field is not lower than 0
#         if (isinstance(data[field], int) or isinstance(data[field], float)) and data[field] < 0:
#             return False, f"The attribute '{field}' cannot be lower than 0!"

#         # Check if list of id contains only integers
#         if isinstance(data[field], list):
#             # Iterate in the list to check each value
#             for ids in data[field]:
#                 if not isinstance(ids, int):
#                     return False, f"Only ID's allowed in the list!"

#     return True, None

def validate_data(data, required):
    """
    Valida si los datos proporcionados contienen todos los campos requeridos y si son válidos.
    
    Args:
    - data (dict): Datos a validar.
    - required (list): Lista de campos requeridos.
    
    Returns:
    - bool: Verdadero si los datos son válidos, falso en caso contrario.
    - str: Mensaje de error o None.
    """
    for field in required:
        # Verificar si el campo existe
        if field not in data:
            return False, f"Falta el campo '{field}' en el JSON."

        # Verificar si el campo de tipo str no está vacío
        if isinstance(data[field], str) and not data[field].strip():
            return False, f"El campo '{field}' no puede estar vacío."

        # Verificar si el campo de tipo int o float no es menor que 0
        if isinstance(data[field], (int, float)) and data[field] < 0:
            return False, f"El campo '{field}' no puede ser menor que 0."

        # Verificar si la lista contiene solo enteros
        if isinstance(data[field], list) and not all(isinstance(ids, int) for ids in data[field]):
            return False, f"El campo '{field}' solo puede contener ID's enteros."

    return True, None
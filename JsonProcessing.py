import json
import re


def getAttributes(jsonString):
    # Devuelve los atributos de un json
    data = json.loads(jsonString)
    return data.keys()

def contiene_json(cadena):
    # Verifica si una cadena es un JSON o contiene JSON
    patronJson = r"\{([^}]*)\}" # Busco el patron entre llaves
    match = re.search(patronJson, cadena)
    if match:
        cadena = match.group()
        cadena = cadena.replace("'", "\"") # Corrijo posible error de comillas
        try:
            json.loads(cadena)
            return cadena
        except json.JSONDecodeError:
            return None
    else:
        return None

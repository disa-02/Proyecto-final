import json
import re


def getAttributes(jsonString):
    # Devuelve los atributos de un json
    data = json.loads(jsonString)
    return data.keys()



def contiene_json(cadena):
    # Verifica si una cadena es un json
    try:
        json.loads(cadena)
        return True
    except json.JSONDecodeError:
        return False

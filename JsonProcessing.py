import json
import re


def getAttributes(jsonString):
    data = json.loads(jsonString)
    return data.keys()



def contiene_json(cadena):
    try:
        json.loads(cadena)
        return True
    except json.JSONDecodeError:
        return False

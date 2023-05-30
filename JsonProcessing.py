import json
import re


def getAttributes(jsonString):
    data = json.loads(jsonString)
    return data.keys()


def parche(cadena):
    datos = cadena.split(':')
    ultimoElemento = datos[-1]
    while (ultimoElemento[-1] == ' '):
        ultimoElemento = ultimoElemento[:-1]

    if (ultimoElemento[-1] != '}'):
        print("entraaaaaaaa")
        if (ultimoElemento[-1] == ','):
            cadena = cadena[:-1]
        cadena = cadena + ']}'
    print(cadena)
    return cadena


def contiene_json(cadena):
    # cadena = parche(cadena)
    try:
        json.loads(cadena)
        return True
    except json.JSONDecodeError:
        return False

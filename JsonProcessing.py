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


# Ejemplo de strings
cadena1 = 'asd {"nombre": "Juan", "edad": 30}'
cadena2 = 'Esto no es un JSON'

print(contiene_json(cadena1))  # True
print(contiene_json(cadena2))  # False


def verificar_json(text):
    print("Texto:\n" + text)
    patron = r'\{.*?\}'
    resultados = re.findall(patron, text)
    print("Resultados:\n" + '\n'.join(resultados))

    finalJson = {}
    for json_str in resultados:
        datos = json.loads(json_str)
        finalJson.update(datos)
    return json.dumps(finalJson)

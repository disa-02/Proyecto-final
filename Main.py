from textProcessing import textProcessing
from ChatGPT import ChatGPT

import yaml


def fileImport(fileName):
    try:
        file = open(fileName, 'r')
        data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print("The file does not exists")
    return None


data = fileImport("openapi.yaml")
x = textProcessing()
descriptions = x.procces(data)
lista = []
cont = 1
for path, endpoint in descriptions.items():
    for method, description in endpoint.items():
        lista.append('' + str(cont) + "-" + description)
        cont += 1
        # print(description)
# print(lista)
chat = ChatGPT()
chat.agrupar(lista)

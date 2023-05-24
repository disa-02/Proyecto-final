import textProcessing
import ChatGPT
import Files


data = Files.filesImport("./openApiDescriptions")
descriptions = []
for d in data:
    descriptions.append(textProcessing.procces(d))
lista = []
cont = 1
for description in descriptions:
    for path, endpoint in description.items():
        for method, description in endpoint.items():
            lista.append('' + str(cont) + "-" + description)
            cont += 1
            # print(description)
# print(lista)
respuesta = ChatGPT.agrupar(lista)
print("Respuesta: \n")
print(respuesta)

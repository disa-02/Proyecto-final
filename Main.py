import textProcessing
import ChatGPTChunks
import Files
from tqdm import tqdm
import JsonProcessing
import json
import Vectorization
import KmeansClustering


# Importacion de los documentos
files = Files.filesImport("./openApiDescriptions")
filesDescriptions = []
vectorDescriptions = []

# Procesamiento de los documentos
con = 0
print("\nProcesando documentos:")
for d in tqdm(files, desc="Documento"):
    filesDescriptions.append(textProcessing.procces(d))
    print("leeen")
    print(len(filesDescriptions[con]))
    con = con + 1

# Obtencion de las descripciones como una lista enumerada
lista = []
cont = 1
for descriptions in filesDescriptions:
    for path, endpoint in descriptions.items():
        for method, description in endpoint.items():
            lista.append('' + str(cont) + "-" + description)
            cont += 1
Files.saveFile("\n".join(lista), "DescripcionesProcesadas.txt", "./outs/", "w")

# Agrupacion con consultas al chatGpt
groupings = ChatGPTChunks.agrupar(lista)
Files.saveFile(
    str(groupings), "AgrupacionDeDescripciones.json", "./outs/", "w")

# Vectorizacion
res = Vectorization.vectorize(groupings, filesDescriptions)
print(res)
# Agregar metodo para guardar el resultado en un archivo y no perder esa info
# FALTA ESTO

# Clustering
data,sse = KmeansClustering.cluster(res, 3)
print("Data")
print(data)
print("SSE")
print(sse)

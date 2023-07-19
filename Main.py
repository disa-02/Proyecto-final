import textProcessing
import ChatGPTChunks
import Files
from tqdm import tqdm
import JsonProcessing
import json
import Vectorization
import KmeansClustering

def enumDescriptions(filesDescriptions):
    lista = []
    cont = 1
    for descriptions in filesDescriptions:
        for path, endpoint in descriptions.items():
            for method, description in endpoint.items():
                lista.append('' + str(cont) + "-" + description)
                cont += 1
    return lista

def generateOutVectorization(res):
    out = ""
    for i in range(0,len(res)):
        out = out + str(filesNames[i]) + ": " + str(res[i]) + "\n"
    return out

def generateOutCluster(data,sse,centroids):
    out = "SSE: " + str(sse) + "\n"
    out = out + "Centroides: " + "\n".join(str(centroids)) + "/n"
    out = out + "\n"
    for i in range(0,3):#k
        out = out + "Group " + str(i) + ":\n"
        for num in range(0,len(data)):
            if(data[num] == i):
                out = out + str(filesNames[num]) + "\n"
        out = out + "\n"
    return out

#---MAIN---
# Importacion de los documentos
files, filesNames = Files.filesImport("./openApiDescriptions")
filesDescriptions = []
vectorDescriptions = []

# Procesamiento de los documentos
con = 0
print("\nProcesando documentos:")
for d in tqdm(files, desc="Documento"):
    filesDescriptions.append(textProcessing.procces(d))
    con = con + 1

# Obtencion de las descripciones como una lista enumerada
lista = enumDescriptions(filesDescriptions)

# Agrupacion con consultas al chatGpt
groupings = ChatGPTChunks.agrupar(lista)

# Vectorizacion
print("Vectorizando archivos...")
res = Vectorization.vectorize(groupings, filesDescriptions)
print(res)

# Clustering
print("Realizando el clustering:")
data,sse,centroids = KmeansClustering.cluster(res, 3)#k


# Save files
Files.saveFile("\n".join(lista), "DescripcionesProcesadas.txt", "./outs/", "w")
Files.saveFile(str(groupings), "AgrupacionDeDescripciones.json", "./outs/", "w")
out = generateOutVectorization(res)
Files.saveFile(out, "vectorizacion.txt", "./outs/", "w")
out = generateOutCluster(data,sse,centroids)
Files.saveFile(out, "finalOut.txt", "./outs/", "w")



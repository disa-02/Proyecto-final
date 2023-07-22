import textProcessing
import ChatGPTChunks
import Files
from tqdm import tqdm
import JsonProcessing
import json
import Vectorization
import KmeansClustering
import time
import sys

def enumDescriptions(filesDescriptions):
    # Enumera las descripciones
    enumFilesDescriptions = []
    cont = 1
    for descriptions in filesDescriptions:
        for path, endpoint in descriptions.items():
            for method, description in endpoint.items():
                enumFilesDescriptions.append('' + str(cont) + "-" + description)
                cont += 1
    return enumFilesDescriptions 

def generateOutVectorization(res):
    # Genera la salida del resultado de vectorizar los documentos
    out = ""
    for i in range(0,len(res)):
        out = out + str(filesNames[i]) + ": " + str(res[i]) + "\n"
    return out

def generateOutCluster(data,sse,centroids):
    # Genera la salida del resultado de aplicar clustering sobre los documentos,es la salida final del programa
    out = ""
    for i in range(0,3):#k
        out = out + "Group " + str(i) + ":\n"
        for num in range(0,len(data)):
            if(data[num] == i):
                out = out + str(filesNames[num]) + "\n"
        out = out + "\n"
    out = out + "\n"
    out = out + "SSE: " + str(sse) + "\n\n"
    out = out + "Centroides: \n" + str(centroids)
    return out

#-----------MAIN-----------
start_time = time.time()

# Lectura de las entradas
entries = Files.openTxt("./entries.txt")
if (len(entries) < 3):
    print("Error en la entrada, no se definieron todos los atributos")
    sys.exit()
chunks = int(entries[0])
k = int(entries[1])
nInit = int(entries[2])

# Importacion de los documentos
files, filesNames = Files.filesImport("./openApiDescriptions")

# Procesamiento de los documentos
filesDescriptions = [] # Almacena todas las descripciones de todos los documentos
print("\nProcesando documentos:")
for d in tqdm(files, desc="Documento"):
    filesDescriptions.append(textProcessing.procces(d))

# Obtencion de las descripciones como una lista enumerada
enumFilesDescriptions = enumDescriptions(filesDescriptions)

# Agrupacion con consultas al chatGpt
groupings = ChatGPTChunks.group(enumFilesDescriptions,chunks)

# Vectorizacion
print("Vectorizando archivos...")
res = Vectorization.vectorize(groupings, filesDescriptions)

# Clustering
print("Realizando el clustering:")
data,sse,centroids = KmeansClustering.cluster(res, k, nInit)


# Save files
Files.saveFile("\n".join(enumFilesDescriptions), "DescripcionesProcesadas.txt", "./outs/", "w")
Files.saveFile(str(groupings), "AgrupacionDeDescripciones.json", "./outs/", "w")
out = generateOutVectorization(res)
Files.saveFile(out, "vectorizacion.txt", "./outs/", "w")
out = generateOutCluster(data,sse,centroids)
Files.saveFile(out, "finalOut.txt", "./outs/", "w")

end_time = time.time()
total_time = end_time - start_time
print("Programa finalizado")
print(f"Tiempo de ejecución: {total_time:.6f} segundos")

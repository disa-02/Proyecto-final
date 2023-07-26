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
import outsGenerator

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


#-----------MAIN-----------
start_time = time.time()

# Lectura de las entradas
entries = Files.openTxt("./entries.txt")
if (len(entries) < 7):
    print("Error en la entrada, no se definieron todos los atributos")
    sys.exit()

chunks = int(entries[0])
# model=str(entries[1])
numberSentences = int(entries[2])
commonWords = int(entries[3])
k = int(entries[4])
nInit = int(entries[5])


# Importacion de los documentos
files, filesNames = Files.filesImport("./openApiDescriptions")

# Procesamiento de los documentos
filesDescriptions = [] # Almacena todas las descripciones de todos los documentos
print("\nProcesando documentos:")
for d in tqdm(files, desc="Documento"):
    filesDescriptions.append(textProcessing.procces(d,commonWords,numberSentences))

# Obtencion de las descripciones como una lista enumerada
enumFilesDescriptions = enumDescriptions(filesDescriptions)

# Agrupacion con consultas al chatGpt
groupings = ChatGPTChunks.group(enumFilesDescriptions,chunks)

# Vectorizacion
print("Vectorizando archivos...")
vectorsGroups, res = Vectorization.vectorize(groupings, filesDescriptions)

# Clustering
print("Realizando el clustering:")
data,sse,centroids = KmeansClustering.cluster(res, k, nInit)


# Save files
Files.saveFile("\n".join(enumFilesDescriptions), "DescripcionesProcesadas.txt", "./outs/", "w")
Files.saveFile(str(groupings), "AgrupacionDeDescripciones.json", "./outs/", "w")
out = outsGenerator.generateOutVectorization(res,filesNames)
Files.saveFile(out, "vectorizacion.txt", "./outs/", "w")
out = outsGenerator.generateOutCluster(data,sse,centroids,k,filesNames)
Files.saveFile(out, "finalOut.txt", "./outs/", "w")
outs = outsGenerator.generateOutFiles(filesDescriptions ,vectorsGroups)
for i in range(0,len(outs)):
    Files.saveFile(outs[i], str(filesNames[i]) + ".txt", "./outs/files/", "w")

# Fin del programa
end_time = time.time()
total_time = end_time - start_time
print("Programa finalizado")
print(f"Tiempo de ejecución: {total_time:.6f} segundos")

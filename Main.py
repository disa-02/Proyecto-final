import textProcessing
import ChatGptGrouping
import ChatGptAssistedGrouping
import Files
from tqdm import tqdm
import JsonProcessing
import json
import Vectorization
import KmeansClustering
import time
import sys
import outsGenerator
import prueba
import ClusteringJerarquico
import SemanticGrouping



def enumDescriptions(filesDescriptions):
    # Enumera las descripciones
    enumFilesDescriptions = []
    cont = 1
    for descriptions in filesDescriptions:
        for path, endpoint in descriptions.items():
            for method, description in endpoint.items():
                if(description is None):
                    description = "none"
                enumFilesDescriptions.append('' + str(cont) + "-" + description)
                cont += 1
    return enumFilesDescriptions 

    
#-----------MAIN-----------
start_time = time.time()
# Inicializacion de las carpetas de salida
Files.deleteFiles("./outs/files/")
Files.deleteFiles("./outs/prompts/")
Files.deleteFiles("./outs/responses/")
Files.saveFile("", "DescripcionesGeneradas.txt", "./outs/", "w") #Lo escribo vacio


# Lectura de las entradas
entries = Files.openTxt("./entries.txt")
if (len(entries) < 13):
    print("Error en la entrada, no se definieron todos los atributos")
    sys.exit()

chunks = int(entries[0])
# model=str(entries[1])
numberSentences = int(entries[2])
commonWords = int(entries[3])
k = int(entries[4])
nInit = int(entries[5])
method=int(entries[9])
kInt=int(entries[7])
nInitInt = int(entries[8])
umbral = float(entries[10])
finalClustering = int(entries[12])

importDocs = 0
filesDescriptions = []
filesNames = []
time2 = 0


print("Importando documentos:")
if (importDocs == 1):
    
    # Importacion de los documentos
    files, filesNames = Files.filesImport("./openApiDescriptions")
    time2I=time.time()
    # Procesamiento de los documentos
    # filesDescriptions = [] # Almacena todas las descripciones de todos los documentos
    print("\nProcesando documentos:")
    for d in tqdm(files, desc="Documento"):
        filesDescriptions.append(textProcessing.procces(d,commonWords,numberSentences))
    time2F=time.time()
    time2=time2F - time2I


else:
    filesDescriptions = Files.cargar_json_como_diccionario("./outs/filesDescriptions.json")
    filesNames = Files.filesImportNames("./openApiDescriptions")

# Obtencion de las descripciones como una lista enumerada
enumFilesDescriptions = enumDescriptions(filesDescriptions)


# Agrupacion de las descripciones
print("Realizando agrupamiento de las descripciones")
groupings = {}
if method == 0: # Usando el chat
    groupings = ChatGptGrouping.group(enumFilesDescriptions, chunks)
elif method == 1: # Usando el chat de manera asistida
    groupings = ChatGptAssistedGrouping.group(enumFilesDescriptions,chunks,umbral)
elif method == 2: # Usando k-means
    groupings = KmeansClustering.groupDescriptions(enumFilesDescriptions, kInt, nInitInt)
elif method == 3:
    groupings = ClusteringJerarquico.groupDescriptions(enumFilesDescriptions, kInt) 
else:
    groupings = SemanticGrouping.group(enumFilesDescriptions,umbral)

# Vectorizacion
print("Vectorizando archivos...")
vectorsGroups, res = Vectorization.vectorize(groupings, filesDescriptions, method)

# Clustering
print("Realizando el clustering:")
if(finalClustering == 0):
    data,error,centroids = KmeansClustering.cluster(res, k, nInit)
else:
    data,error,centroids = ClusteringJerarquico.cluster(res, k)
# Save files
Files.guardar_diccionario_en_json(filesDescriptions, "./outs/filesDescriptions.json")
Files.saveFile("\n".join(enumFilesDescriptions), "DescripcionesProcesadas.txt", "./outs/", "w")
Files.saveFile(str(groupings), "AgrupacionDeDescripciones.json", "./outs/", "w")
out = outsGenerator.generateOutVectorization(res,filesNames)
Files.saveFile(out, "vectorizacion.txt", "./outs/", "w")
out = outsGenerator.generateOutCluster(data,error,centroids,k,filesNames)
Files.saveFile(out, "finalOut.txt", "./outs/", "w")
outs = outsGenerator.generateOutFiles(filesDescriptions ,vectorsGroups)
for i in range(0,len(outs)):
    Files.saveFile(outs[i], str(filesNames[i]) + ".txt", "./outs/files/", "w")

# Fin del programa
print("Tiempo de procesamiento de descripciones")
print(time2)
end_time = time.time()
total_time = end_time - start_time
print("Programa finalizado")
print(f"Tiempo de ejecución: {total_time:.6f} segundos")
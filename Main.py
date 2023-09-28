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

def initFiles():
    Files.deleteFiles("./outs/files/")
    Files.deleteFiles("./outs/prompts/")
    Files.deleteFiles("./outs/responses/")
    Files.saveFile("", "DescripcionesGeneradas.txt", "./outs/", "w") #Lo escribo vacio

def readEntries():
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
    return chunks,numberSentences,commonWords,k,nInit,method,kInt,nInitInt,umbral,finalClustering

def docImport(importDocs, commonWords,numberSentences):
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
    return filesDescriptions,filesNames,time2

def groupDescriptions(enumFilesDescriptions,chunks,umbral,kInt,nInitInt,method):
    groupings = {}
    score = -5
    if method == 0: # Usando el chat
        groupings = ChatGptGrouping.group(enumFilesDescriptions, chunks)
    elif method == 1: # Usando el chat de manera asistida
        groupings = ChatGptAssistedGrouping.group(enumFilesDescriptions,chunks,umbral)
    elif method == 2: # Usando k-means
        groupings,score = KmeansClustering.groupDescriptions(enumFilesDescriptions, kInt, nInitInt)
    elif method == 3: # Usando clustering jerarquico
        groupings,score = ClusteringJerarquico.groupDescriptions(enumFilesDescriptions, kInt) 
    else: # Usando agrupacion semantica
        groupings = SemanticGrouping.group(enumFilesDescriptions,umbral)
    return groupings,score

def saveFiles(filesDescriptions,enumFilesDescriptions,res,filesNames,data,error,k,vectorsGroups,outFolder,time,score):
    Files.guardar_diccionario_en_json(filesDescriptions, "./" + outFolder + "/filesDescriptions.json")
    Files.saveFile("\n".join(enumFilesDescriptions), "DescripcionesProcesadas.txt", "./" + outFolder + "/", "w")
    Files.saveFile(str(groupings), "AgrupacionDeDescripciones.json", "./" + outFolder + "/", "w")
    out = outsGenerator.generateOutVectorization(res,filesNames)
    Files.saveFile(out, "vectorizacion.txt", "./" + outFolder + "/", "w")
    out = outsGenerator.generateOutCluster(data,error,k,filesNames,time,score)
    Files.saveFile(out, "finalOut.txt", "./" + outFolder + "/", "w")
    outs = outsGenerator.generateOutFiles(filesDescriptions ,vectorsGroups)
    for i in range(0,len(outs)):
        Files.saveFile(outs[i], str(filesNames[i]) + ".txt", "./" + outFolder + "/" + "files/", "w")

#-----------MAIN-----------
start_time = time.time()
# Inicializacion de las carpetas de salida
initFiles()

# Lectura de las entradas
chunks,numberSentences,commonWords,k,nInit,method,kInt,nInitInt,umbral,finalClustering = readEntries()

#Importacion de los documentos de entrada
importDocs = 0
filesDescriptions,filesNames,time2 = docImport(importDocs, commonWords,numberSentences)

# Obtencion de las descripciones como una lista enumerada
enumFilesDescriptions = enumDescriptions(filesDescriptions)

# Agrupacion de las descripciones
print("Realizando agrupamiento de las descripciones")
groupings,score = groupDescriptions(enumFilesDescriptions,chunks,umbral,kInt,nInitInt,method)

# Vectorizacion
print("Vectorizando archivos...")
vectorsGroups, res = Vectorization.vectorize(groupings, filesDescriptions, method)

# Clustering
print("Realizando el clustering:")
if(finalClustering == 0):
    data,error = KmeansClustering.cluster(res, k, nInit)
else:
    data,error = ClusteringJerarquico.cluster(res, k)

end_time = time.time()
total_time = end_time - start_time

# Save files
saveFiles(filesDescriptions,enumFilesDescriptions,res,filesNames,data,error,k,vectorsGroups,"outs",total_time,score)

# Fin del programa
print("Tiempo de procesamiento de descripciones")
print(time2)
total_time = end_time - start_time
print("Programa finalizado")
print(f"Tiempo de ejecución: {total_time:.6f} segundos")
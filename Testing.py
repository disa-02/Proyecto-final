import Main
import time
import ChatGptAssistedGrouping
import KmeansClustering
import ClusteringJerarquico
import SemanticGrouping
import Vectorization


init_time = time.time()
Main.initFiles()
# Lectura de las entradas
chunks,numberSentences,commonWords,k,nInit,method,kInt,nInitInt,umbral,finalClustering = Main.readEntries()

#Importacion de los documentos de entrada
importDocs = 1
generate = 0
filesDescriptions,filesNames,time2 = Main.docImport(importDocs, commonWords,numberSentences,generate)

# Obtencion de las descripciones como una lista enumerada
enumFilesDescriptions = Main.enumDescriptions(filesDescriptions)

init_time = time.time() - init_time

# Agrupacion de las descripciones
groupTime = time.time()
groupingsKmeans,scoreKmeans = KmeansClustering.groupDescriptions(enumFilesDescriptions, kInt, nInitInt)
timeKmeans = time.time() - groupTime + init_time

groupTime = time.time()
groupingsJerarquico,scoreJerarquico = ClusteringJerarquico.groupDescriptions(enumFilesDescriptions, kInt) 
timeJerarquico = time.time() - groupTime + init_time

groupTime = time.time()
groupingsSemantic,scoreSemantic = SemanticGrouping.group(enumFilesDescriptions,umbral)
timeSemantic = time.time() - groupTime + init_time

groupTime = time.time()
groupingsChatAssisted = ChatGptAssistedGrouping.group(enumFilesDescriptions,chunks,umbral)
scoreChat = -5
timeChat = time.time() - groupTime + init_time

# Vectorizacion
print("Vectorizando archivos...")
vectorTime = time.time()
vectorsGroupsChatAssisted, resChatAssisted = Vectorization.vectorize(groupingsChatAssisted, filesDescriptions, 1)
timeChat = time.time() - vectorTime + timeChat

vectorTime = time.time()
vectorsGroupsKmeans, resKmeans = Vectorization.vectorize(groupingsKmeans, filesDescriptions, 2)
timeKmeans = time.time() - vectorTime + timeKmeans

vectorTime = time.time()
vectorsGroupsJerarquico, resJerarquico = Vectorization.vectorize(groupingsJerarquico, filesDescriptions, 3)
timeJerarquico = time.time() - vectorTime + timeJerarquico

vectorTime = time.time()
vectorsGroupsSemantic, resSemantic = Vectorization.vectorize(groupingsSemantic, filesDescriptions, 4)
timeSemantic = time.time() - vectorTime + timeSemantic


# Clustering final
print("Realizando el clustering:")
# ChatAssisted
k = 5
clusterTime = time.time()
data,error = KmeansClustering.cluster(resChatAssisted, k, nInit)
finalTime = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Kmeans_5",finalTime,scoreChat,groupingsChatAssisted)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resChatAssisted, k)
finalTime = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Jerarquico_5",finalTime,scoreChat,groupingsChatAssisted)

k = 10
clusterTime = time.time()
data,error = KmeansClustering.cluster(resChatAssisted, k, nInit)
finalTime = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Kmeans_10",finalTime,scoreChat,groupingsChatAssisted)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resChatAssisted, k)
finalTime = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Jerarquico_10",finalTime,scoreChat,groupingsChatAssisted)

k = 15
clusterTime = time.time()
data,error = KmeansClustering.cluster(resChatAssisted, k, nInit)
finalTime = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Kmeans_15",finalTime,scoreChat,groupingsChatAssisted)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resChatAssisted, k)
finalTime = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Jerarquico_15",finalTime,scoreChat,groupingsChatAssisted)

k = 20
clusterTime = time.time()
data,error = KmeansClustering.cluster(resChatAssisted, k, nInit)
finalTime = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Kmeans_20",finalTime,scoreChat,groupingsChatAssisted)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resChatAssisted, k)
finalTime = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Jerarquico_20",finalTime,scoreChat,groupingsChatAssisted)

# Kmeans
k = 5
clusterTime = time.time()
data,error = KmeansClustering.cluster(resKmeans, k, nInit)
finalTime = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Kmeans_5",finalTime,scoreKmeans,groupingsKmeans)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resKmeans, k)
finalTime = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Jerarquico_5",finalTime,scoreKmeans,groupingsKmeans)

k = 10
clusterTime = time.time()
data,error = KmeansClustering.cluster(resKmeans, k, nInit)
finalTime = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Kmeans_10",finalTime,scoreKmeans,groupingsKmeans)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resKmeans, k)
finalTime = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Jerarquico_10",finalTime,scoreKmeans,groupingsKmeans)

k = 15
clusterTime = time.time()
data,error = KmeansClustering.cluster(resKmeans, k, nInit)
finalTime = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Kmeans_15",finalTime,scoreKmeans,groupingsKmeans)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resKmeans, k)
finalTime = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Jerarquico_15",finalTime,scoreKmeans,groupingsKmeans)

k = 20
clusterTime = time.time()
data,error = KmeansClustering.cluster(resKmeans, k, nInit)
finalTime = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Kmeans_20",finalTime,scoreKmeans,groupingsKmeans)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resKmeans, k)
finalTime = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Jerarquico_20",finalTime,scoreKmeans,groupingsKmeans)

# Jerarquico
k=5
clusterTime = time.time()
data,error = KmeansClustering.cluster(resJerarquico, k, nInit)
finalTime = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Kmeans_5",finalTime,scoreJerarquico,groupingsJerarquico)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resJerarquico, k)
finalTime = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Jerarquico_5",finalTime,scoreJerarquico,groupingsJerarquico)

k = 10
clusterTime = time.time()
data,error = KmeansClustering.cluster(resJerarquico, k, nInit)
finalTime = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Kmeans_10",finalTime,scoreJerarquico,groupingsJerarquico)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resJerarquico, k)
finalTime = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Jerarquico_10",finalTime,scoreJerarquico,groupingsJerarquico)

k = 15
clusterTime = time.time()
data,error = KmeansClustering.cluster(resJerarquico, k, nInit)
finalTime = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Kmeans_15",finalTime,scoreJerarquico,groupingsJerarquico)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resJerarquico, k)
finalTime = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Jerarquico_15",finalTime,scoreJerarquico,groupingsJerarquico)

k = 20
clusterTime = time.time()
data,error = KmeansClustering.cluster(resJerarquico, k, nInit)
finalTime = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Kmeans_20",finalTime,scoreJerarquico,groupingsJerarquico)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resJerarquico, k)
finalTime = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Jerarquico_20",finalTime,scoreJerarquico,groupingsJerarquico)

# Semantic
k=5
clusterTime = time.time()
data,error = KmeansClustering.cluster(resSemantic, k, nInit)
finalTime = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Kmeans_5",finalTime,scoreSemantic,groupingsSemantic)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resSemantic, k)
finalTime = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Jerarquico_5",finalTime,scoreSemantic,groupingsSemantic)

k = 10
clusterTime = time.time()
data,error = KmeansClustering.cluster(resSemantic, k, nInit)
finalTime = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Kmeans_10",finalTime,scoreSemantic,groupingsSemantic)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resSemantic, k)
timeSemantic = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Jerarquico_10",finalTime,scoreSemantic,groupingsSemantic)

k = 15
clusterTime = time.time()
data,error = KmeansClustering.cluster(resSemantic, k, nInit)
finalTime = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Kmeans_15",finalTime,scoreSemantic,groupingsSemantic)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resSemantic, k)
finalTime = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Jerarquico_15",finalTime,scoreSemantic,groupingsSemantic)

k = 20
clusterTime = time.time()
data,error = KmeansClustering.cluster(resSemantic, k, nInit)
finalTime = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Kmeans_20",finalTime,scoreSemantic,groupingsSemantic)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resSemantic, k)
finalTime = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Jerarquico_20",finalTime,scoreSemantic,groupingsSemantic)

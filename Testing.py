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
importDocs = 0
filesDescriptions,filesNames,time2 = Main.docImport(importDocs, commonWords,numberSentences)

# Obtencion de las descripciones como una lista enumerada
enumFilesDescriptions = Main.enumDescriptions(filesDescriptions)

init_time = time.time() - init_time

# Agrupacion de las descripciones
groupTime = time.time()
groupingsChatAssisted,scoreChat = ChatGptAssistedGrouping.group(enumFilesDescriptions,chunks,umbral)
timeChat = time.time() - groupTime + init_time

groupTime = time.time()
groupingsKmeans,scoreKmeans = KmeansClustering.groupDescriptions(enumFilesDescriptions, kInt, nInitInt)
timeKmeans = time.time() - groupTime + init_time

groupTime = time.time()
groupingsJerarquico,scoreJerarquico = ClusteringJerarquico.groupDescriptions(enumFilesDescriptions, kInt) 
timeJerarquico = time.time() - groupTime + init_time

groupTime = time.time()
groupingsSemantic,scoreSemantic = SemanticGrouping.group(enumFilesDescriptions,umbral)
timeSemantic = time.time() - groupTime + init_time

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


# Clustering
print("Realizando el clustering:")
# ChatAssisted
k = 5
clusterTime = time.time()
data,error = KmeansClustering.cluster(resChatAssisted, k, nInit)
timeChat = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Kmeans_5",timeChat,scoreChat)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resChatAssisted, k)
timeChat = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Jerarquico_5",timeChat,scoreChat)

k = 10
clusterTime = time.time()
data,error = KmeansClustering.cluster(resChatAssisted, k, nInit)
timeChat = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Kmeans_10",timeChat,scoreChat)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resChatAssisted, k)
timeChat = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Jerarquico_10",timeChat,scoreChat)

k = 15
clusterTime = time.time()
data,error = KmeansClustering.cluster(resChatAssisted, k, nInit)
timeChat = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Kmeans_15",timeChat,scoreChat)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resChatAssisted, k)
timeChat = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Jerarquico_15",timeChat,scoreChat)

k = 20
clusterTime = time.time()
data,error = KmeansClustering.cluster(resChatAssisted, k, nInit)
timeChat = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Kmeans_20",timeChat,scoreChat)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resChatAssisted, k)
timeChat = time.time() - clusterTime + timeChat
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resChatAssisted,filesNames,data,error,k,vectorsGroupsChatAssisted,"outs_ChatAssisted_Jerarquico_20",timeChat,scoreChat)

# Kmeans
k = 5
clusterTime = time.time()
data,error = KmeansClustering.cluster(resKmeans, k, nInit)
timeKmeans = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Kmeans_5",timeKmeans,scoreKmeans)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resKmeans, k)
timeKmeans = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Jerarquico_5",timeKmeans,scoreKmeans)

k = 10
clusterTime = time.time()
data,error = KmeansClustering.cluster(resKmeans, k, nInit)
timeKmeans = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Kmeans_10",timeKmeans,scoreKmeans)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resKmeans, k)
timeKmeans = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Jerarquico_10",timeKmeans,scoreKmeans)

k = 15
clusterTime = time.time()
data,error = KmeansClustering.cluster(resKmeans, k, nInit)
timeKmeans = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Kmeans_15",timeKmeans,scoreKmeans)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resKmeans, k)
timeKmeans = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Jerarquico_15",timeKmeans,scoreKmeans)

k = 20
clusterTime = time.time()
data,error = KmeansClustering.cluster(resKmeans, k, nInit)
timeKmeans = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Kmeans_20",timeKmeans,scoreKmeans)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resKmeans, k)
timeKmeans = time.time() - clusterTime + timeKmeans
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resKmeans,filesNames,data,error,k,vectorsGroupsKmeans,"outs_Kmeans_Jerarquico_20",timeKmeans,scoreKmeans)

# Jerarquico
k=5
clusterTime = time.time()
data,error = KmeansClustering.cluster(resJerarquico, k, nInit)
timeJerarquico = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Kmeans_5",timeSemantic,scoreJerarquico)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resJerarquico, k)
timeJerarquico = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Jerarquico_5",timeSemantic,scoreJerarquico)

k = 10
clusterTime = time.time()
data,error = KmeansClustering.cluster(resJerarquico, k, nInit)
timeJerarquico = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Kmeans_10",timeSemantic,scoreJerarquico)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resJerarquico, k)
timeJerarquico = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Jerarquico_10",timeSemantic,scoreJerarquico)

k = 15
clusterTime = time.time()
data,error = KmeansClustering.cluster(resJerarquico, k, nInit)
timeJerarquico = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Kmeans_15",timeSemantic,scoreJerarquico)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resJerarquico, k)
timeJerarquico = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Jerarquico_15",timeSemantic,scoreJerarquico)

k = 20
clusterTime = time.time()
data,error = KmeansClustering.cluster(resJerarquico, k, nInit)
timeJerarquico = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Kmeans_20",timeSemantic,scoreJerarquico)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resJerarquico, k)
timeJerarquico = time.time() - clusterTime + timeJerarquico
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resJerarquico,filesNames,data,error,k,vectorsGroupsJerarquico,"outs_Jerarquico_Jerarquico_20",timeSemantic,scoreJerarquico)

# Semantic
k=5
clusterTime = time.time()
data,error = KmeansClustering.cluster(resSemantic, k, nInit)
timeSemantic = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Kmeans_5",timeSemantic,scoreSemantic)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resSemantic, k)
timeSemantic = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Jerarquico_5",timeSemantic,scoreSemantic)

k = 10
clusterTime = time.time()
data,error = KmeansClustering.cluster(resSemantic, k, nInit)
timeSemantic = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Kmeans_10",timeSemantic,scoreSemantic)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resSemantic, k)
timeSemantic = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Jerarquico_10",timeSemantic,scoreSemantic)

k = 15
clusterTime = time.time()
data,error = KmeansClustering.cluster(resSemantic, k, nInit)
timeSemantic = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Kmeans_15",timeSemantic,scoreSemantic)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resSemantic, k)
timeSemantic = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Jerarquico_15",timeSemantic,scoreSemantic)

k = 20
clusterTime = time.time()
data,error = KmeansClustering.cluster(resSemantic, k, nInit)
timeSemantic = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Kmeans_20",timeSemantic,scoreSemantic)

clusterTime = time.time()
data,error = ClusteringJerarquico.cluster(resSemantic, k)
timeSemantic = time.time() - clusterTime + timeSemantic
Main.saveFiles(filesDescriptions,enumFilesDescriptions,resSemantic,filesNames,data,error,k,vectorsGroupsSemantic,"outs_Semantic_Jerarquico_20",timeSemantic,scoreSemantic)

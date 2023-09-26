import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from sklearn.preprocessing import normalize
from sklearn.metrics import silhouette_score



def cluster(data,k,nInit):
    
    data = normalize(data)

    # Realiza un clustering con el metodo k-means utilizando k clusters en un set de data
    kmeans = KMeans(n_clusters=k,n_init=nInit)

    # solo funciona para representar elementos de dos dimensiones
    # plt.scatter(data[:,0],data[:,1],c=kmeans.labels_.astype(float),s=50)
    # plt.scatter(centroids[:,0], centroids[:,1],c='red',marker='*',s=50)
    # plt.show()

    clust=kmeans.fit_predict(data)
    centroids = kmeans.cluster_centers_
    sse = kmeans.inertia_
    print("Silhoutte")
    score = silhouette_score(data, kmeans.labels_)
    print(score)

    return clust,sse,centroids

def clusterK(data,nInit):
    # Realiza un clustering sobre un set de data calculando el mejor k --> FALTA TERMINAR
    krange = range(1,len(data))
    sse = []
    for k in krange:
        kmeans = KMeans(n_clusters=k,n_init=nInit).fit(data)
        sse.append(kmeans.inertia_) 
    
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.plot(krange,sse)
    plt.show()

def groupDescriptions(textos,n_clusters,nIntit):
    # Crea un objeto TfidfVectorizer para convertir los textos en vectores TF-IDF
    vectorizador = TfidfVectorizer(stop_words="english")
    vectores = vectorizador.fit_transform(textos)
    # print(vectores)
    voc = vectorizador.get_feature_names_out()

    vectores = normalize(vectores)
    vectores = vectores.toarray()
 
    # vectores = removeOutliers(vectores)
    

    # Crea una instancia del algoritmo KMeans
    kmeans = KMeans(n_clusters=n_clusters,n_init=nIntit)

    # Agrupa los textos según los centroides más cercanos
    labels = kmeans.fit_predict(vectores)
    print("Silhoutte")
    score = silhouette_score(vectores, kmeans.labels_)
    print(score)
    # Crea un diccionario para almacenar los textos por etiqueta (label)
    grupos = {}
    for label, texto in zip(labels, textos):
        if label not in grupos:
            grupos[int(label)] = []
        grupos[int(label)].append(int(texto.split("-")[0]))

    return grupos

# data = np.random.random(size=(30,2)) #30 puntos de 2 dimensiones
# result,sse = cluster(data, 4)
# print(result)
# print(sse)
# # clusterK(data)

def removeOutliers(datos):
    # Calcular el primer cuartil (Q1) y el tercer cuartil (Q3)
    q1 = np.percentile(datos, 25)
    q3 = np.percentile(datos, 75)

    # Calcular el rango intercuartílico (IQR)
    iqr = q3 - q1

    # Definir los límites inferior y superior para identificar outliers
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    # Filtrar los datos para eliminar los outliers
    datos_filtrados = [x for x in datos if limite_inferior <= x <= limite_superior]

    return datos_filtrados
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def cluster(data,k,nInit):
    # Realiza un clustering con el metodo k-means utilizando k clusters en un set de data
    kmeans = KMeans(n_clusters=k,n_init=nInit).fit(data)
    centroids = kmeans.cluster_centers_
    # print(centroids)

    # solo funciona para representar elementos de dos dimensiones
    # plt.scatter(data[:,0],data[:,1],c=kmeans.labels_.astype(float),s=50)
    # plt.scatter(centroids[:,0], centroids[:,1],c='red',marker='*',s=50)
    # plt.show()

    clust=kmeans.predict(data)
    sse = kmeans.inertia_
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


# data = np.random.random(size=(30,2)) #30 puntos de 2 dimensiones
# result,sse = cluster(data, 4)
# print(result)
# print(sse)
# # clusterK(data)
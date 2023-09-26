import numpy as np
# import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score

from sklearn.preprocessing import normalize
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram

import Files

def removeOutliers(data):
  # Calcula la media de cada fila.
    means = data.mean(axis=1)
    # Cambia la forma del segundo operando para que coincida con la forma del primer operando.
    means = means[:, np.newaxis]
    # Calcula la distancia entre cada punto y la media de su fila.
    distances = np.linalg.norm(data - means, axis=1)
    # Identifica los puntos que se encuentran a una distancia mayor que el umbral.
    outliers = distances > 10
    # Elimina los outliers del arreglo.
    data = data[~outliers]
    return data

def cluster(data,k):
    # Realiza un clustering con el metodo k-means utilizando k clusters en un set de data
    data_scaled = normalize(data)

   
    
    cluster = AgglomerativeClustering(n_clusters=k,metric='euclidean', linkage='ward')
    cluster.fit_predict(data_scaled)
    labels = cluster.labels_

    silhouette = silhouette_score(data_scaled, labels)

    return labels,silhouette, None


def groupDescriptions(textos,n_clusters):
    vectorizador = TfidfVectorizer()
    vectores = vectorizador.fit_transform(textos)
    vectores = normalize(vectores)
    vectores = vectores.toarray()
    model = AgglomerativeClustering(n_clusters=n_clusters,distance_threshold=None)

    # Entrenamos el modelo
    model.fit_predict(vectores)

    labels = model.labels_

    silhouette = silhouette_score(vectores, labels)
    print(silhouette)
    
    grupos = {}
    for label, texto in zip(labels, textos):
        if label not in grupos:
            grupos[int(label)] = []
        grupos[int(label)].append(int(texto.split("-")[0]))
    return grupos


import numpy as np
# import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score

from sklearn.preprocessing import normalize
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import pandas as pd
from scipy.spatial import distance

import Files



def cluster(data,k):
    # Realiza un clustering con el metodo k-means utilizando k clusters en un set de data
    # data = normalize(data)

    cluster = AgglomerativeClustering(n_clusters=k,metric='euclidean', linkage='ward')
    clust = cluster.fit_predict(data)
    labels = cluster.labels_

    score = silhouette_score(data, labels)

    return labels,score


def groupDescriptions(textos,n_clusters):
    vectorizador = TfidfVectorizer()
    vectores = vectorizador.fit_transform(textos)
    vectores = normalize(vectores)
    vectores = vectores.toarray()
    labels,score = cluster(vectores,n_clusters)

    grupos = {}
    for label, texto in zip(labels, textos):
        if label not in grupos:
            grupos[int(label)] = []
        grupos[int(label)].append(int(texto.split("-")[0]))
    return grupos,score


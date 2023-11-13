import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans as KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from sklearn.preprocessing import normalize
from sklearn.metrics import silhouette_score



def cluster(data,k,nInit):
    
    # data = normalize(data)

    # Realiza un clustering con el metodo k-means utilizando k clusters en un set de data
    kmeans = KMeans(n_clusters=k,n_init=nInit)

    clust=kmeans.fit_predict(data)
    score = silhouette_score(data, kmeans.labels_)

    return clust,score



def groupDescriptions(textos,n_clusters,nIntit):
    # Crea un objeto TfidfVectorizer para convertir los textos en vectores TF-IDF
    vectorizador = TfidfVectorizer(stop_words="english")
    vectores = vectorizador.fit_transform(textos)
    voc = vectorizador.get_feature_names_out()

    vectores = normalize(vectores)
    vectores = vectores.toarray()
 
    labels,score = cluster(vectores,n_clusters,nIntit) 


    # Crea un diccionario para almacenar los textos por etiqueta (label)
    grupos = {}
    for label, texto in zip(labels, textos):
        if label not in grupos:
            grupos[int(label)] = []
        grupos[int(label)].append(int(texto.split("-")[0]))

    return grupos,score


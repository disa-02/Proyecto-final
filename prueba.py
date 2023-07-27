import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import json

# Define los textos
textos2 = ["1 - El perro es un mamífero","4 - El perro es un mamífero" ,"2-El gato es un mamífero", "3-El caballo es un mamífero"]

def agrupar(textos):
    # Crea un objeto TfidfVectorizer para convertir los textos en vectores TF-IDF
    vectorizador = TfidfVectorizer()
    vectores = vectorizador.fit_transform(textos)

    # Crea una instancia del algoritmo KMeans
    n_clusters = 25
    kmeans = KMeans(n_clusters=n_clusters)

    # Agrupa los textos según los centroides más cercanos
    labels = kmeans.fit_predict(vectores)

    # Crea un diccionario para almacenar los textos por etiqueta (label)
    grupos = {}
    for label, texto in zip(labels, textos):
        if label not in grupos:
            grupos[int(label)] = []
        grupos[int(label)].append(int(texto.split("-")[0]))

    # Convierte el diccionario en formato JSON
    # resultado_json = json.dumps(grupos, indent=4)
    # return str(resultado_json).replace("\n", "").replace(" ", "")
    return grupos

# resp = agrupar(textos2)
# print(resp)
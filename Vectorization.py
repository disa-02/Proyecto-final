import numpy as np
import spac


def _searchGroup(groupings, descriptionNumber):
    # Busca el grupo al que pertenece una descripcion
    data = groupings
    for group, descriptions in data.items():
        if descriptionNumber in descriptions:
            return group
    return None  # Si todo funciona bien nunca deberia entrar aca


def _createVectorByGroup(groupings):
    # Genera un vector por cada grupo -> grupo1:(1,0,0), grupo1:(0,1,0), grupo3:(0,0,1) ...
    vectorGroups = {}
    groups = groupings.keys()
    cont = 0
    for group in groups:
        vector = np.zeros(len(groups))
        vector[cont] = 1
        vectorGroups[group] = vector
        cont = cont + 1
    return vectorGroups

def _createVectorByGroupWhitSemanticRelation(groupings):
    # Genera un vector por cada grupo -> grupo1:(1,0,0), grupo1:(0,1,0), grupo3:(0,0,1) ...
    vectorGroups = {}
    groups = groupings.keys()
    for group in groups:
        vector = np.zeros(len(groups))
        pos = 0
        processGroup = group.replace("_"," ")
        processGroup = group.replace("-"," ")
        for group2 in groups:
            processGroup2 = group2.replace("_"," ")
            processGroup2 = group2.replace("-"," ")
            similitary = spac.anlizeSimilitary(processGroup, processGroup2)
            vector[pos] = similitary
            pos = pos + 1
        vectorGroups[group] = vector
    return vectorGroups

def _assignVectorToDescription(groupings, filesDescriptions, vectorGroups, longVector):
    # Asigna a cada descripcion el vector de grupo correspondiente
    vectorsDescriptions = []
    cont = 1
    for description in filesDescriptions:
        vectors = []
        for path, endpoint in description.items():
            for method, desc in endpoint.items():
                group = _searchGroup(groupings, cont)
                if (group == None): # Si no encuentra grupo pone el vector 0
                    vectors.append(np.zeros(longVector))
                else:
                    vectors.append(vectorGroups.get(group))
                cont = cont + 1
        vectorsDescriptions.append(vectors)
    return vectorsDescriptions


def _addVectors(vectors):
    # Suma todos los vectores de un mismo archivo openApi
    addition = np.zeros(len(vectors[0]))
    for vector in vectors:
        # print(vector)
        addition = addition + vector
    # Evaluar cuando se haga el clustering si conviene hacer esta division
    addition = addition / len(vectors)
    return addition


def vectorize(groupings, filesDescriptions,method):
    # Vectoriza los archivos openApi segun sus operaciones
    longVector = len(groupings.keys())
    vectorGroups = []
    if method >=  2:
        vectorGroups = _createVectorByGroup(groupings)
    else:
        vectorGroups = _createVectorByGroupWhitSemanticRelation(groupings)

    vectorsDescriptions = _assignVectorToDescription(groupings, filesDescriptions, vectorGroups, longVector)
    # cont = 1
    # out = ""
    vectorDescriptionsAddition = []
    for vectors in vectorsDescriptions:
        addition = _addVectors(vectors)
        vectorDescriptionsAddition.append(addition)
        # cont = cont + 1
    # outliers(vectorDescriptionsAddition)
    # vectorDescriptionsAddition = delCeros(vectorDescriptionsAddition)
    return vectorsDescriptions,vectorDescriptionsAddition

import numpy as np
from scipy import stats


def outliers(data):

    

    if isinstance(data, list):
        data = np.array(data)
    # Calcular el Z-Score para cada punto en tus datos
    z_scores = np.abs(stats.zscore(data))

    # Definir un umbral para identificar outliers (puedes ajustarlo según tus necesidades)
    umbral = 2.0

    # Encontrar los índices de los puntos que son outliers
    outlier_indices = []
    for i in range(len(z_scores)):
        if all(z_scores[i] > umbral):
            outlier_indices.append(i)

    # Obtener los puntos que son outliers
    outliers = data[outlier_indices]
    print(outliers)
    print(outlier_indices)

def countCeros(vectores):
    longV = len(vectores[0])
    cerosVector = []
    for j in range(0,longV):
        ceros = 0
        for vector in vectores:
            if(vector[j] == 0):
                ceros = ceros + 1
        percent = ceros/len(vectores)
        cerosVector.append(percent)
    return cerosVector

        
def delCeros(vectores):
    vectores = vectores
    ceros = countCeros(vectores)
    i = 0
    j = 0
    for i in range(len(ceros)):
        percent = ceros[i]
        if(percent > 0.8):
            for vector in vectores:
                del vector[j]
        else:
            j = j + 1
    return vectores


import numpy as np


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


def vectorize(groupings, filesDescriptions):
    # Vectoriza los archivos openApi segun sus operaciones
    longVector = len(groupings.keys())
    vectorGroups = _createVectorByGroup(groupings)
    vectorsDescriptions = _assignVectorToDescription(groupings, filesDescriptions, vectorGroups, longVector)
    cont = 1
    out = ""
    vectorDescriptionsAddition = []
    for vectors in vectorsDescriptions:
        addition = _addVectors(vectors)
        vectorDescriptionsAddition.append(addition)
        cont = cont + 1
    return vectorsDescriptions,vectorDescriptionsAddition

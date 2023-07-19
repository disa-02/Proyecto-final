import numpy as np


def _searchGroup(groupings, descriptionNumber):
    data = groupings  # json.loads(groupings)
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
    vectorsDescriptions = []
    cont = 1
    for description in filesDescriptions:
        vectors = []
        for path, endpoint in description.items():
            for method, desc in endpoint.items():
                group = _searchGroup(groupings, cont)
                if (group == None):
                    vectors.append(np.zeros(longVector))
                else:
                    vectors.append(vectorGroups.get(group))
                cont = cont + 1
        vectorsDescriptions.append(vectors)
    return vectorsDescriptions


def _addVectors(vectors):
    addition = np.zeros(len(vectors[0]))
    for vector in vectors:
        # print(vector)
        addition = addition + vector
        # Evaluar cuando se haga el clustering si conviene hacer esta division
        addition = addition / len(vectors)
    return addition


def vectorize(groupings, filesDescriptions):
    vectorDescriptions = []
    longVector = len(groupings.keys())
    vectorGroups = _createVectorByGroup(groupings)
    vectorsDescriptions = _assignVectorToDescription(groupings, filesDescriptions, vectorGroups, longVector)
    cont = 1
    out = ""
    for vectors in vectorsDescriptions:
        # print("File " + str(cont) + ":")
        # print("Len:" + str(len(vectors)))
        addition = _addVectors(vectors)
        vectorDescriptions.append(addition)
        # print("Sum vectors:")
        # print(addition)
        # print()
        cont = cont + 1
    return vectorDescriptions

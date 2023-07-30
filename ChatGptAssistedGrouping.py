import os
import JsonProcessing
import time
from tqdm import tqdm
import ChatOperations
import Files


main_statemenet = """Dada una lista de temas identificados numéricamente, agruparlos según su relación semántica en grupos bien definidos y representativos. Un tema no puede pertenecer a mas de un grupo; no puede haber temas no agrupados y no puede haber un mismo tema en grupos diferentes.
La respuesta se presentará en formato JSON, donde cada atributo será el nombre del grupo y el valor una lista numérica de los temas correspondientes.
Es importante que los nombres de los grupos sean descriptivos y representen claramente la temática de los temas que agrupan. Asimismo, trata de evitar de que los grupos contengan un único tema.\n"""


def groupUngroupedDescriptions(ungroupedDescriptions,groups,assistedGroups,umbral):
    if ungroupedDescriptions != None:
            if len(groups) > 0:
                document, group = ChatOperations.groupTopics(ungroupedDescriptions,groups,umbral)
                assistedGroups.update(group)
                values = []
                for doc in document:
                    values.append(int(doc.split("-")[0]))
                assistedGroups.setdefault("others",[]).extend(values)   


def group(enumFilesDescriptions,chunks,umbral):
    # Agrupa las descripciones segun su relacion semantica utilizando el chat
    
    finalResponse = []
    cont = 0

    # Separacion de las descripciones en la cantidad de tokens especificados
    documents = ChatOperations.createChunks(enumFilesDescriptions,chunks)

    # Consultas
    print("Realizando consultas a chatGPT:")    
    groups = set() # Grupos que se generan en cada consulta 
    assistedGroups = {} # Diccionario que almacena los grupos y los valores matcheados sin el chat (con spacy)
    ungroupedDescriptions = [] # Descripciones que no se pudieron agrupar
    for document in tqdm(documents, desc="Consulta"):
        # Agrupacion de descripciones sin utilizar el chat
        if len(groups) > 0:
            document, group = ChatOperations.groupTopics(document,groups,umbral)
            assistedGroups.update(group)

        # Agrupacion de descripciones restantes(no agrupadas en el paso anterior) en nuevos grupos con el chat (consulta al chat)
        prompt = main_statemenet + '\n'.join(document)
        response = ChatOperations.consult(prompt)
        finalResponse.append(response)

        # Obtengo las descripciones que no fueron agrupadas por el chat
        ungruped = ChatOperations.getUngropedDescriptions(document, response, enumFilesDescriptions)
        ungroupedDescriptions.extend(ungruped)
        
        # Obtengo los grupos de la respuesta del chat
        newGroups = JsonProcessing.getAttributes(response)
        groups.update(set(newGroups))

        # Guardado de la consulta
        Files.saveFile(prompt, "prompt_" + str(cont) + ".txt", "./outs/prompts/", "w")
        cont = cont + 1

    # Agrupo los grupos que nunca se agruparon
    groupUngroupedDescriptions(ungroupedDescriptions,groups,assistedGroups,umbral)
    assistedGroups = str(assistedGroups)
    assistedGroups = assistedGroups.replace("'", "\"")
    finalResponse.append(str(assistedGroups))

    ChatOperations.saveFiles(finalResponse)
    finalResponse = ChatOperations.generateResponseFinal(finalResponse)
    return finalResponse

import os
import JsonProcessing
import time
from tqdm import tqdm
import Files
import ChatOperations

main_statemenet = """Agrupar temas por su relación semántica en un JSON con nombres de grupo representativos
Dada una lista de temas identificados numéricamente, agruparlos según su relación semántica en grupos bien definidos y representativos. Cada tema debe pertenecer a un único grupo; no puede haber temas no agrupados. La respuesta se presentará en formato JSON, donde cada atributo será el nombre del grupo y el valor una lista numérica de los temas correspondientes.
Es importante que los nombres de los grupos sean descriptivos y representen claramente la temática de los temas que agrupan. Asimismo, trata de evitar de que las agrupaciones  contengan grupos con un único tema.\n"""

def group(enumFilesDescriptions,chunks):
    # Agrupa las descripciones segun su relacion semantica utilizando el chat

    finalResponse = []
    cont = 0

    # Separacion de las descripciones en la cantidad de tokens especificado
    documents = ChatOperations.createChunks(enumFilesDescriptions,chunks)

    # Primera consulta
    print("Realizando consultas a chatGPT:")
    prompt = main_statemenet + ('\n'.join(documents[0]))
    response = ChatOperations.consult(prompt)
    finalResponse.append(response)

    documents.pop(0)
    Files.saveFile(prompt, "prompt_" + str(cont) + ".txt", "./outs/prompts/", "w")
    
    # Resto de consultas
    groups = set() # Grupos que se generan en cada consulta 
    for document in tqdm(documents, desc="Consulta"):
        # Obtengo los grupos de la consulta anterior
        newGroups = JsonProcessing.getAttributes(response)
        groups.update(set(newGroups))

        # Agrupacion de las descripciones teniendo en cuenta los grupos ya creados utilizando el chat
        prompt = f"\nConsiderando que ya existen los siguientes grupos.\n{' '.join(f'{i+1}-{elem}' for i, elem in enumerate(groups))} \nAnalizar si los siguientes temas pueden pertenecer a uno de estos grupos. En caso que haya temas que no pertenece a ningun grupo, agruparlos según su relación semántica en grupos bien definidos y representativos. Cada tema debe pertenecer a un único grupo; no puede haber temas no agrupados. La respuesta se presentará en formato JSON, donde cada atributo será el nombre del grupo y el valor una lista numérica de los temas correspondientes.Es importante que los nombres de los grupos sean descriptivos y representen claramente la temática de los temas que agrupan. Asimismo, trata de evitar de que las agrupaciones contengan grupos con un único tema.\n""" + '\n'.join(document) 
        response = ChatOperations.consult(prompt)
        finalResponse.append(response)

        # Guardado de la consulta
        cont = cont + 1
        Files.saveFile(prompt, "prompt_" + str(cont) + ".txt", "./outs/prompts/", "w")

    ChatOperations.saveFiles(finalResponse)
    finalResponse = ChatOperations.generateResponseFinal(finalResponse)
    return finalResponse

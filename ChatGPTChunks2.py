import os
import openai
import JsonProcessing
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from tqdm import tqdm
import Files
import spac
import json
import copy
import spac

openai.api_key = str(Files.openTxt("./entries.txt")[6])

main_statemenet = """Agrupar temas por su relación semántica en un JSON con nombres de grupo representativos
Dada una lista de temas identificados numéricamente, agruparlos según su relación semántica en grupos bien definidos y representativos. Cada tema debe pertenecer a un único grupo; no puede haber temas no agrupados. La respuesta se presentará en formato JSON, donde cada atributo será el nombre del grupo y el valor una lista numérica de los temas correspondientes.
Es importante que los nombres de los grupos sean descriptivos y representen claramente la temática de los temas que agrupan. Asimismo, asegúrate de que las agrupaciones no contengan grupos con un único tema y de evitar el uso de saltos de línea o espacios en la respuesta.\n"""


def createChunks(filesDescriptions,chunks):
    # Divide el texto segun cantidad de caracteres especificados
    char_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunks, chunk_overlap=0)
    docs = char_text_splitter.split_text(filesDescriptions)
    return docs

def checkAttributes(response):
    # Verifica la respuesta generada por el chat, verifica que los nombres de los grupos sean representativos
    atributos = JsonProcessing.getAttributes(response)
    for element in atributos:
        if "group" in element.lower() or "grupo" in element.lower():
            return True
    return False


def consult(prompt):
    # Realiza la consulta al chat
    condition = True
    response = ''
    while (condition):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ])
            response = (completion.choices[0].message.content)
            response = JsonProcessing.contiene_json(response)
            if (response != None):
                if (not checkAttributes(response)):
                    condition = False
                else:
                    print("Error en la generacion de los nombres en la respuesta, reintentando ...")
            else:
                print("Error en el formato de la respuesta, reintentando ...")
        except openai.error.RateLimitError as error:
            print("Error de tiempo al agrupar, reintentando ...")
            time.sleep(5)
        except openai.error.ServiceUnavailableError as e:
            print("Error: El servidor está sobrecargado o no está listo todavía, reintentando...")
            time.sleep(5)
    return response

def generateResponseFinal(finalResponse):
    # Procesa todas las respuestas del chat y lo convierte en un json con la respuesta final
    resp = {}
    for response in finalResponse:
        response_data = json.loads(response)
        for key, value in response_data.items():
            if key in resp:
                # Agregar los elementos a la lista existente
                resp[key].extend(value)
            else:
                # Crear una nueva lista para la clave
                resp[key] = value  
    return resp

def saveFiles(finalResponse):
    # Genera un json por cada respuesta del chat
    cont = 0
    for response in finalResponse:
        Files.saveFile(response, "response_" + str(cont) +
                       ".json", "./outs/responses/", "w")
        cont = cont + 1

def getPreviousResults(response,filesDescriptions):
    result = []
    jsonResponse = json.loads(response)
    for key in jsonResponse.keys():
        if len(jsonResponse[key]) > 0:
            pos = jsonResponse[key][0]
            pos = pos - 1
            desc = str(filesDescriptions[pos])
            result.append(desc)
        else:
            print(f"Warning: se genero un grupo vacio - {key}")
    return result

def joinResponses(response,previousResults,respAnt,filesDescriptions):
    respAnt = json.loads(respAnt)
    keysRespAnt = list(respAnt.keys())
    response = json.loads(response)
    cont = 0
    delete = []
    add = {}
    deletes = {}
    for searchValue in previousResults:
        searchValue = int(searchValue.split("-")[0])
        for key in response.keys():
            for value in response[key]:
                if(value == searchValue):
                    newKey = keysRespAnt[cont]
                    umbral = spac.anlizeSimilitary(key, newKey)
                    print(f"key1:{key} - key2:{newKey} - umbral:{umbral}")
                    if(umbral > 0.7):
                        print("ENTRAAA")
                        response[key].remove(value)
                        delete.append(key)
                        if newKey in add:
                            # Agregar los elementos a la lista existente
                            add[newKey].extend(response[key])
                        else:
                            # Crear una nueva lista para la clave
                            add[newKey] = response[key]  
                        cont = cont + 1
                    else:
                        umbral1 = spac.anlizeSimilitary(filesDescriptions[value-1], newKey)
                        umbral2 = spac.anlizeSimilitary(filesDescriptions[value-1], key)
                        if umbral1 > umbral2:
                            # response[key] = response[key].remove(value) #analizar en cual esta mejor
                            print("borra")
                        else:
                            if newKey in deletes:
                                # Agregar los elementos a la lista existente
                                deletes[newKey].extend(value)
                            else:
                                # Crear una nueva lista para la clave
                                deletes[newKey] = value  
    for key in delete:
        if key in response.keys():
            response.pop(key)
        else:
            print(f"La llave no existe{key}")
    for key in add.copy().keys():
        if len(add[key]) == 0:
            add.pop(key)
    response.update(add)
    response = str(response)
    response = response.replace("'", "\"")
    return response, deletes

def group(filesDescriptions,chunks):
    # Agrupa las descripciones segun su relacion semantica utilizando el chat
    documents = createChunks("\n".join(["".join(text) for text in filesDescriptions]),chunks)
    finalResponse = []
    print("Realizando consultas a chatGPT:")
    previousResults = []
    cont = 0
    response = ""
    for document in tqdm(documents, desc="Consulta"):
        # Obtengo los grupos de la consulta anterior
        # newGroups = JsonProcessing.getAttributes(response)
        # groups.update(set(newGroups))
        respAnt = response
        document = "\n".join(previousResults) + document
        prompt = main_statemenet + document
                                            
        
        Files.saveFile(prompt, "prompt_" + str(cont) +
                       ".txt", "./outs/prompts/", "w")
        cont = cont + 1
        response = consult(prompt)
        if len(respAnt) > 0:
            response,deletes = joinResponses(response,previousResults,respAnt,filesDescriptions)
        # ult = len(finalResponse) -1
        # ultResponse = finalResponse[ult]
        # for key,value in deletes:
        #     ultResponse[key] = list(set(ultResponse[key]) - set(value))
        # finalResponse[ult] = ultResponse
        finalResponse.append(response)
        previousResults = getPreviousResults(response,filesDescriptions)

    saveFiles(finalResponse)
    # Files.saveFile(str(agrupaciones), "agrupaciones.json", "./outs/", "w")
    finalResponse = generateResponseFinal(finalResponse)
    return finalResponse

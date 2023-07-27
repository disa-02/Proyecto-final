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

openai.api_key = str(Files.openTxt("./entries.txt")[6])

main_statemenet = """Agrupar temas por su relación semántica en un JSON con nombres de grupo representativos
Dada una lista de temas identificados numéricamente, agruparlos según su relación semántica en grupos bien definidos y representativos. Cada tema debe pertenecer a un único grupo; no puede haber temas no agrupados. La respuesta se presentará en formato JSON, donde cada atributo será el nombre del grupo y el valor una lista numérica de los temas correspondientes.
Es importante que los nombres de los grupos sean descriptivos y representen claramente la temática de los temas que agrupan. Asimismo, trata de evitar de que las agrupaciones  contengan grupos con un único tema.\n"""


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

def checkRepeatedTopics(response):
    repeated = set()
    dic = json.loads(response)
    for key in dic:
        valores = dic[key]
        for valor in valores:
            if valor in repeated:
                return True
            repeated.add(valor)
    return False

def consult(prompt):
    # Realiza la consulta al chat
    condition = True
    response = ''
    while (condition):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
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
                if (not checkRepeatedTopics(response)):
                    condition = False
                else:
                    print("Error se genero un json con valores repetidos, reintentando ...")
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

def group(filesDescriptions,chunks):
    # Agrupa las descripciones segun su relacion semantica utilizando el chat
    documents = createChunks("\n".join(["".join(text) for text in filesDescriptions]),chunks)
    finalResponse = []
    print("Realizando consultas a chatGPT:")

    # Primera consulta
    cont = 0
    prompt = main_statemenet + (documents[0])
    Files.saveFile(prompt, "prompt_" + str(cont) +
                   ".txt", "./outs/prompts/", "w")
    response = consult(prompt)
    documents.pop(0)
    finalResponse.append(response)
    # Resto de consultas
    groups = set()
    for document in tqdm(documents, desc="Consulta"):
        # Obtengo los grupos de la consulta anterior
        newGroups = JsonProcessing.getAttributes(response)
        groups.update(set(newGroups))

        prompt = f"\nConsiderando que ya existen los siguientes grupos.\n{' '.join(f'{i+1}-{elem}' for i, elem in enumerate(groups))} \nAnalizar si los siguientes temas pueden pertenecer a uno de estos grupos. En caso que haya temas que no pertenece a ningun grupo, agruparlos según su relación semántica en grupos bien definidos y representativos. Cada tema debe pertenecer a un único grupo; no puede haber temas no agrupados. La respuesta se presentará en formato JSON, donde cada atributo será el nombre del grupo y el valor una lista numérica de los temas correspondientes.Es importante que los nombres de los grupos sean descriptivos y representen claramente la temática de los temas que agrupan. Asimismo, trata de evitar de que las agrupaciones contengan grupos con un único tema.\n""" + document
                                            
        cont = cont + 1
        Files.saveFile(prompt, "prompt_" + str(cont) +
                       ".txt", "./outs/prompts/", "w")
        response = consult(prompt)
        finalResponse.append(response)

    saveFiles(finalResponse)
    # Files.saveFile(str(agrupaciones), "agrupaciones.json", "./outs/", "w")
    finalResponse = generateResponseFinal(finalResponse)
    return finalResponse

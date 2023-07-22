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

openai.api_key = "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"

main_statemenet = """Dado los siguientes temas. Agruparlos según su relación semántica. 
                Los temas si o si deben pertenecer a un unico grupo. No pueden haber temas no agrupados.
                Dar la respuesta en un json  donde cada atributo sea el nombre de grupo y el valor una lista de los temas. 
                La lista de temas debe ser unicamente numerica y cada numero debe corresponder al 
                identificador de cada tema, no debe haber strings en este atributo.
                No utilices saltos de lineas ni espacios en la respuesta.
                Intenta que en las agrupaciones no queden grupos con un unico tema.
                Lista de temas:  """
#El nombre de grupo debe ser representativo a los temas que agrupa. 

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
            if (JsonProcessing.contiene_json(response)):
                # if (not checkAttributes(response)):
                #     condition = False
                condition = False # si agrego el if borrar esta linea
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
    documents = createChunks(" ".join(["".join(text) for text in filesDescriptions]),chunks)
    finalResponse = []
    print("Realizando consultas a chatGPT:")

    # Primera consulta
    cont = 0
    prompt = main_statemenet + documents[0]
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

        prompt = main_statemenet + document + """Considerar que ya existen los siguientes grupos como atributos del json.
                                            Analizar si un tema puede pertenecer a uno de estos grupos o es necesario agruparlo en uno nuevo.
                                            Debes tener en cuenta la relacion semantica de cada tema: """ + ' '.join(f'{i+1}-{elem}' for i, elem in enumerate(grupos))
        cont = cont + 1
        Files.saveFile(prompt, "prompt_" + str(cont) +
                       ".txt", "./outs/prompts/", "w")
        response = consult(prompt)
        finalResponse.append(response)

    saveFiles(finalResponse)
    # Files.saveFile(str(agrupaciones), "agrupaciones.json", "./outs/", "w")
    finalResponse = generateResponseFinal(finalResponse)
    return finalResponse

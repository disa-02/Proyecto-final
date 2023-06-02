import os
import openai
import JsonProcessing
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from tqdm import tqdm
import Files
import spac

openai.api_key = "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"

main_enunciado = "Dado los siguientes temas. Agrupa sus elementos según su relación semántica.Los temas no pueden pertenecer a mas de un grupo. Dar la respuesta en un json  donde cada atributo sea el nombre de grupo y el valor una lista de los temas. El nombre de grupo debe ser representativo a los temas que agrupa. La lista de temas debe ser unicamente numerica y cada numero debe corresponder al identificador de cada tema, no debe haber strings en este atributo.No utilices saltos de lineas ni espacios en la respuesta.Intenta que en las agrupaciones no queden grupos con un unico tema.Lista de temas:  "


def createChunks(lista):
    char_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=0)
    docs = char_text_splitter.split_text(lista)
    print(len(docs))
    return docs


def getResponseGroups(response):
    groups = JsonProcessing.getAttributes(response)
    return groups


def consultar(prompt):
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
                condition = False
            print("Condition=" + str(condition))
        except openai.error.RateLimitError as error:
            print("error de tiempo")
            time.sleep(5)
    return response


def generarResponseFinal(finalResponse):
    resp = {}
    for response in finalResponse:
        response_data = json.loads(response)
        for key, value in response_data.items():
            if key in resp:
                # Agregar los elementos a la lista existente
                resp[key].extend(value)
            else:
                resp[key] = value  # Crear una nueva lista para la clave
    return resp


def saveFiles(finalResponse):
    cont = 0
    for response in finalResponse:
        Files.saveFile(response, "response_" + str(cont) +
                       ".json", "./outs/responses/")
        cont = cont + 1


def agruparYaExistentes(grupos, document):
    agrupaciones = {}
    similitudFinal = -1
    grupoFinal = ''
    print("Verificando si las descripciones pertenecen a grupo ya creado")
    for item in tqdm(document, desc="Descripcion"):
        for grupo in grupos:
            similitud = spac.anlizar_similutud(item, grupo)
            if (similitudFinal < similitud):
                similitudFinal = similitud
                grupoFinal = grupo
        if (similitudFinal > 0.8):
            document.remove(item)
            if grupoFinal in agrupaciones:
                # Agregar los elementos a la lista existente
                agrupaciones[grupoFinal].append(item[0])
            else:
                # Crear una nueva lista para la clave
                agrupaciones[grupoFinal] = [item[0]]
    return agrupaciones, document


def agrupar(lista):
    document, lista = spac.getTextTokens(lista)
    finalResponse = []
    print("Realizando consultas a chatGPT:")

    # Primera consulta
    cont = 0
    prompt = main_enunciado + " ".join(document)
    Files.saveFile(prompt, "prompt_" + str(cont) + ".txt", "./outs/prompts/")
    response = consultar(prompt)
    finalResponse.append(response)

    # Resto de consultas
    grupos = set()
    agrupaciones = {}
    while (len(lista) != 0):
        # Obtengo los grupos de la consulta anterior
        newGroups = getResponseGroups(response)
        grupos.update(set(newGroups))

        # Verifico si algun tema pertenece a grupos ya creados
        agrupaciones, lista = agruparYaExistentes(grupos, lista)

        document, lista = spac.getTextTokens(lista)

        prompt = main_enunciado + \
            " ".join(document) + """Considerar que ya existen los siguientes grupos como atributos del json.Analizar si un tema puede pertenecer a uno de estos grupos o es necesario agruparlo en uno nuevo.Debes tener en cuenta la relacion semantica de cada tema: """ + ' '.join(grupos)
        cont = cont + 1
        Files.saveFile(prompt, "prompt_" + str(cont) +
                       ".txt", "./outs/prompts/")
        response = consultar(prompt)
        finalResponse.append(response)
        print("entro")
    saveFiles(finalResponse)
    Files.saveFile(agrupaciones, "agrupaciones.json", "./outs/")
    finalResponse = generarResponseFinal(finalResponse)
    return finalResponse

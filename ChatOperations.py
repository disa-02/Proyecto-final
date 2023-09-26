import openai
import JsonProcessing
import json
import Files
import spac

openai.api_key = str(Files.openTxt("./entries.txt")[6])

def createChunks(enumFilesDescriptions,chunks):
    # Separa todas las descripciones en chunks del tamano especificado
    documents = []
    chars = 0
    chunk = []
    for description in enumFilesDescriptions:
        lenDescription = len(description)
        if lenDescription + chars > chunks:
            documents.append(chunk)
            chunk = []
            chars = 0
        chunk.append(description)
        chars = chars + lenDescription
    documents.append(chunk)
    return documents

def _checkAttributes(response):
    # Verifica la respuesta generada por el chat, verifica que los nombres de los grupos sean representativos
    atributos = JsonProcessing.getAttributes(response)
    for element in atributos:
        if "group" in element.lower() or "grupo" in element.lower():
            return True
    return False

def _checkRepeatedTopics(response):
    repeated = set()
    dic = json.loads(response)
    for key in dic:
        valores = dic[key]
        for valor in valores:
            if valor in repeated:
                return True
            repeated.add(valor)
    return False

def _delRepeatedTopics(response):
    repeated = set()
    dic = json.loads(response)
    for key in dic:
        valores = dic[key].copy()
        i = 0
        for valor in valores:
            if valor in repeated:
                del dic[key][i]
            else:
                i = i+1
                repeated.add(valor)
    return json.dumps(dic)

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
                response = _delRepeatedTopics(response)
                if (not _checkAttributes(response)):
                    # if (not _checkRepeatedTopics(response)):
                    condition = False
                    # else:
                    #     print("Error se genero un json con valores repetidos, reintentando ...")
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

def groupTopics(document,groups,umbral):
    # Agrupa las descripciones en los grupos dados segun su relacion semantica
    finalGroups = {}
    # docs = document.split("\n")
    otherDocs = []
    for doc in document: #docs
        value = int(doc.split("-")[0])
        text = str(doc.split("-")[1])

        similitary = 0
        finalGroup = ""
        for group in groups:
            processGroup = group.replace("_"," ")
            processGroup = group.replace("-"," ")
            newSimilitary = spac.anlizeSimilitary(text, processGroup)
            if newSimilitary > similitary:
                similitary = newSimilitary
                finalGroup = group
        if similitary > umbral:
            finalGroups.setdefault(finalGroup,[]).extend([value])        
        else:
            otherDocs.append(doc)
    return otherDocs,finalGroups

def getUngropedDescriptions(document, response, enumFilesDescriptions):
    # Obtiene las descripciones que no fueron agrupadas en la respuesta del chat
    ungroupedResponses = []
    descriptionsNumbers = []
    responseNumbers = []
    # Se obtienen los identificadores de las descripciones
    for description in document:
        number = int(description.split("-")[0])
        descriptionsNumbers.append(number)
    # Se obtienen los valores de la respuesta
    jsonResponse = json.loads(response)
    for key,values in jsonResponse.items():
        responseNumbers.extend(values)
    
    # Chequeo que las descripciones se encuentren en la respuesta
    for number in descriptionsNumbers:
        if number not in responseNumbers:
            ungroupedResponses.append(number)
    rta = []
    for ungrouped in ungroupedResponses:
        rta.append(enumFilesDescriptions[ungrouped - 1])
    return rta
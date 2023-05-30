import os
import openai
import JsonProcessing
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter

openai.api_key = "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"

main_enunciado = """Dado los siguientes temas. Agrupa sus elementos según su relación semántica. 
                Intenta que en las agrupaciones no queden grupos con un unico tema.
                Lista de temas:  """
respuesta = """Se debe cumplir estrictamente el siguiente formato de respuesta: 
            Dar la respuesta en un json  donde cada atributo sea el nombre de grupo y el valor una lista de los temas.
            La lista de temas debe empezar con [ y finalizar con ]. 
            El json debe empezar con { y finalizar con }.
            El json no debe tener espacios.
            Ejemplo de formato de respuesta: {atributo1:[1,3,5,7],atributo2:[2,4,6]}
            """
restricciones = """Restricciones:
                El nombre de grupo debe ser representativo a los temas que agrupa. 
                La lista de temas debe ser unicamente numerica y cada numero debe corresponder al 
                identificador de cada tema, no debe haber strings en este atributo.
                Los temas no pueden pertenecer a mas de un grupo."""


def createChunks(lista):
    char_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=15000, chunk_overlap=0)
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
            if (condition):
                print(response)
            print("Condition=" + str(condition))
        # print(response)
        except openai.error.RateLimitError as error:
            print("error de tiempo")
            time.sleep(5)
    return response


def agrupar(lista):
    documents = createChunks(" ".join(["".join(text) for text in lista]))
    finalResponse = []

    # Primera consulta
    prompt = main_enunciado + documents[0] + respuesta + restricciones
    response = consultar(prompt)
    documents.pop(0)
    finalResponse.append(response)

    # Resto de consultas
    grupos = set()
    for document in documents:
        newGroups = getResponseGroups(response)
        grupos.update(set(newGroups))
        print(grupos)
        print("\n")
        prompt = main_enunciado + document + respuesta + restricciones + """Considerar que ya existen los siguientes grupos como atributos del json.
                                            Analizar si un tema puede pertenecer a uno de estos grupos o es necesario agruparlo en uno nuevo.
                                            Debes tener en cuenta la relacion semantica de cada tema """ + ' '.join(grupos)
        response = consultar(prompt)
        finalResponse.append(response)
    print("Final response\n" + '\n'.join(finalResponse) + "\n")

    return response

import Files
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
import ChatGptDescriptions
import json

from sklearn.feature_extraction.text import CountVectorizer
import spac

nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')


def _extractDescriptions(data, descriptions, pathInfo):
    # Extrae todas las descripciones de todos los documentos
    paths = data.get("paths", {})
    for path, endpoint in paths.items():
        infoDescriptions = {}
        methodInfo = {}
        for method, info in endpoint.items():
            if isinstance(info, dict):
                description = info.get("description")
                infoDescriptions[method] = description
                if (description == None or description == ''):
                    methodInfo[method] = info.items()
                    pathInfo[path] = methodInfo
        descriptions[path] = infoDescriptions

def _completeDescriptions(descriptions, pathInfo,generate):
    # Completa las descripciones faltantes utilizando chatGPT
    for path, endpoint in pathInfo.items():
        for method, description in endpoint.items():
            desc = ""
            if(generate == 1):
                # Request to chatGPT
                prompt = str(path) + ": " + str(method) + ": " + str(description)
                desc = ChatGptDescriptions.generateDescription(prompt)
                Files.saveFile("path: " + str(path) + ":\n" + "operacion: " + str(method) + "\n" + json.dumps(dict(description)) + "\n\n" + "Descripcion generada: " +
                        desc + "\n\n", "DescripcionesGeneradas.txt", "./outs/", "a")
            else:
                desc = None
            descriptions[path][method] = desc

        

 
def _extract_main_topic(path, method, description, descriptions,commonWords):
    text = spac.analyzeSentence(description,commonWords)
    text = ' '.join(text)
    descriptions[path][method] = text


def generateSummary(number_sentences, path, method, description, descriptions):
    # Tokenizar el texto en oraciones
    sentences = sent_tokenize(description)

    # Calcular la frecuencia de las palabras
    frequency = FreqDist(description)

    # Ordenar las oraciones según la suma de las frecuencias de las palabras en cada oración
    ordered_sentences = sorted(sentences, key=lambda oracion: sum(
        frequency[word] for word in word_tokenize(oracion.lower()) if word.isalnum()), reverse=True)

    # Tomar las primeras n oraciones como resumen
    summary = ' '.join(ordered_sentences[:number_sentences])

    descriptions[path][method] = summary


def procces(data,commonWords,numberSentences,generate):
    # Procesa las descripciones obteniendo los tokens mas relevantes
    descriptions = {}
    pathInfo = {}
    _extractDescriptions(data, descriptions, pathInfo)
    _completeDescriptions(descriptions, pathInfo,generate)
    for path, endpoint in descriptions.items():
        for method, description in endpoint.items():
            # generateSummary(numberSentences, path, method, description,descriptions)
            if(description is not None):
                _extract_main_topic(path, method, description, descriptions,commonWords)
    return descriptions

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
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')


def _extractDescriptions(data, descriptions, pathInfo):
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


def _completeDescriptions(descriptions, pathInfo):
    Files.saveFile("", "DescripcionesGeneradas.txt", "./outs/", "w")
    for path, endpoint in pathInfo.items():
        for method, description in endpoint.items():
            # desc = request to chatGPT
            prompt = str(path) + ": " + str(method) + ": " + str(description)
            desc = ChatGptDescriptions.generateDescription(prompt)
            descriptions[path][method] = desc
            Files.saveFile("path: " + str(path) + ":\n" + "operacion: " + str(method) + "\n" + json.dumps(dict(description)) + "\n\n" + "Descripcion generada: " +
                           desc + "\n\n", "DescripcionesGeneradas.txt", "./outs/", "a")


def _delStopWords(path, method, description):
    if (description != None):
        # Tokenizacion
        text = word_tokenize(description)
        # Eliminacion de las stopWords
        for word in text:
            if (word in stopwords.words('english')):
                text.remove(word)
        descriptions[path][method] = text


def _joinDescriptions(path, method, description):
    description = ' '.join(descriptions)
    descriptions[path][method] = description


def _extract_main_topic(path, method, description, descriptions):
    text = spac.analizar_oracion(description)
    text = ' '.join(text)
    descriptions[path][method] = text


def generar_resumen(numero_oraciones, path, method, description):
    # Tokenizar el texto en oraciones
    oraciones = sent_tokenize(description)

    # Calcular la frecuencia de las palabras
    frecuencia = FreqDist(description)

    # Ordenar las oraciones según la suma de las frecuencias de las palabras en cada oración
    oraciones_ordenadas = sorted(oraciones, key=lambda oracion: sum(
        frecuencia[palabra] for palabra in word_tokenize(oracion.lower()) if palabra.isalnum()), reverse=True)

    # Tomar las primeras n oraciones como resumen
    resumen = ' '.join(oraciones_ordenadas[:numero_oraciones])

    descriptions[path][method] = resumen


def procces(data):
    descriptions = {}
    pathInfo = {}
    _extractDescriptions(data, descriptions, pathInfo)
    _completeDescriptions(descriptions, pathInfo)
    for path, endpoint in descriptions.items():
        for method, description in endpoint.items():
            # _delStopWords(path, method, description)
            # _joinDescriptions(path, method, description)
            # generar_resumen(1, path, method, description)
            _extract_main_topic(path, method, description, descriptions)
    return descriptions

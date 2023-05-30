import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize


from sklearn.feature_extraction.text import CountVectorizer
import spac

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
descriptions = {}
pathInfo = {}


def _extractDescriptions(data):
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


def _completeDescriptions():
    for path, endpoint in pathInfo.items():
        for method, description in endpoint.items():
            # desc = request to chatGPT
            desc = "Description generated with chatGPT"
            descriptions[path][method] = desc


def _delStopWords():
    for path, endpoint in descriptions.items():
        for method, description in endpoint.items():
            if (description != None):
                # Tokenizacion
                text = word_tokenize(description)
                # Eliminacion de las stopWords
                for word in text:
                    if (word in stopwords.words('english')):
                        text.remove(word)
            descriptions[path][method] = text


def _joinDescriptions():
    for path, endpoint in descriptions.items():
        for method, description in endpoint.items():
            description = ' '.join(description)
            descriptions[path][method] = description


def _extract_main_topic():
    for path, endpoint in descriptions.items():
        for method, description in endpoint.items():
            text = spac.analizar_oracion(description)
            text = ' '.join(text)
            # print(text)
            descriptions[path][method] = text


def generar_resumen(numero_oraciones):
    for path, endpoint in descriptions.items():
        for method, description in endpoint.items():
            # Tokenizar el texto en oraciones
            oraciones = sent_tokenize(description)

            # # Tokenizar el texto en palabras y filtrar las palabras irrelevantes
            # palabras = word_tokenize(texto.lower())
            # palabras_filtradas = [palabra for palabra in palabras if palabra.isalnum() and palabra not in stopwords.words('spanish')]

            # Calcular la frecuencia de las palabras
            frecuencia = FreqDist(description)

            # Ordenar las oraciones según la suma de las frecuencias de las palabras en cada oración
            oraciones_ordenadas = sorted(oraciones, key=lambda oracion: sum(
                frecuencia[palabra] for palabra in word_tokenize(oracion.lower()) if palabra.isalnum()), reverse=True)

            # Tomar las primeras n oraciones como resumen
            resumen = ' '.join(oraciones_ordenadas[:numero_oraciones])

            descriptions[path][method] = resumen


def analizar_oracion():
    for path, endpoint in descriptions.items():
        for method, description in endpoint.items():
            # Tokenizar la oración en palabras
            palabras = word_tokenize(description)

            # Filtrar palabras irrelevantes (stop words)
            palabras_filtradas = [palabra.lower(
            ) for palabra in palabras if palabra.lower() not in stopwords.words('spanish')]

            # Etiquetar partes del discurso
            palabras_etiquetadas = nltk.pos_tag(palabras_filtradas, lang='es')

            # Calcular la frecuencia de las palabras
            frecuencia = FreqDist(palabras_etiquetadas)

            # Obtener las palabras más relevantes
            palabras_relevantes = [palabra for palabra,
                                   _ in frecuencia.most_common(5)]

            descriptions[path][method] = palabras_relevantes


def procces(data):
    _extractDescriptions(data)
    _completeDescriptions()
    # for path, endpoint in descriptions.items():
    #     for method, description in endpoint.items():
    #         print(description)
    _delStopWords()

    _joinDescriptions()

    generar_resumen(1)

    _extract_main_topic()
    return descriptions

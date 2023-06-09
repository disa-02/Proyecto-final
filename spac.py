import spacy
import re
from nltk.probability import FreqDist
from spacy.lang.es.stop_words import STOP_WORDS


# Cargar el modelo de spaCy en español
nlp = spacy.load('es_core_news_md')


def _filtrar_vector(vector):
    vector_filtrado = []
    for texto in vector:
        # Eliminar caracteres especiales y espacios en blanco
        texto_filtrado = re.sub(r'[^\w\s]|[\n,\'\s\t]', '', texto)
        vector_filtrado.append(texto_filtrado)
    return vector_filtrado


def analizar_oracion(oracion):
    # Procesar la oración con el modelo cargado
    doc = nlp(oracion)

    # Filtrar palabras irrelevantes (stop words)
    palabras_filtradas = [token.lemma_.lower(
    ) for token in doc if not token.is_stop and not token.is_punct]
    palabras_filtradas = _filtrar_vector(palabras_filtradas)
    # Calcular la frecuencia de las palabras
    frecuencia = FreqDist(palabras_filtradas)
    # Obtener las palabras más relevantes
    palabras_relevantes = [palabra for palabra,
                           _ in frecuencia.most_common(5)]
    return palabras_relevantes


def anlizar_similutud(texto, grupo):
    doc_texto = nlp(texto)
    doc_descripcion = nlp(grupo)
    print("aaa")
    print(texto)
    print(grupo)
    print(doc_texto)
    print(doc_descripcion)

    similitud = doc_texto.similarity(doc_descripcion)
    return similitud
    # # Establece un umbral de similitud para considerar que la descripción pertenece al texto
    # umbral_similitud = 0.8

    # if similitud > umbral_similitud:
    #     return True
    # else:
    #     return False


def getTextTokens(lista):
    respuesta = []
    cantidad_tokens = 0
    for item in lista:
        doc = nlp(item)
        if (cantidad_tokens + len(doc) > 1900):
            break
        cantidad_tokens = cantidad_tokens + len(doc)
        respuesta.append(item)
        lista.remove(item)
    return respuesta, lista

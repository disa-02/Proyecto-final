import spacy
from nltk.probability import FreqDist
from spacy.lang.es.stop_words import STOP_WORDS


# Cargar el modelo de spaCy en español
nlp = spacy.load('es_core_news_sm')


def text(texto):
    # Procesar el texto con spaCy
    doc = nlp(texto)

    # Obtener las palabras relevantes basadas en su lema y categoría gramatical
    palabras_relevantes = []
    for token in doc:
        # Filtrar por categorías gramaticales relevantes, como sustantivos y adjetivos
        if token.pos_ in ['NOUN', 'PROPN', 'ADJ']:
            # Agregar el lema de la palabra
            palabras_relevantes.append(token.lemma_)

    # Imprimir las palabras más relevantes
    return palabras_relevantes


def analizar_oracion(oracion):

    # Procesar la oración con el modelo cargado
    doc = nlp(oracion)

    print("aca")
    # Filtrar palabras irrelevantes (stop words)
    palabras_filtradas = [token.lemma_.lower(
    ) for token in doc if not token.is_stop and not token.is_punct]

    print("esooos")
    # Calcular la frecuencia de las palabras
    frecuencia = FreqDist(palabras_filtradas)
    print("sisis")
    # Obtener las palabras más relevantes
    palabras_relevantes = [palabra for palabra, _ in frecuencia.most_common(5)]
    print("ahi sale")
    return palabras_relevantes

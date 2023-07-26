import spacy
import re
from nltk.probability import FreqDist
import Files

model = str(Files.openTxt("./entries.txt")[1])
# Cargar el modelo de spaCy en español
# nlp = spacy.load('es_core_news_md')

# Cargar el modelo de spacy en ingles
nlp = spacy.load(model)


def _filterVector(vector):
    # Elimina caracteres especiales y espacios en blanco
    filter_vector = []
    for text in vector:
        filter_text = re.sub(r'[^\w\s]|[\n,\'\s\t]', '', text)
        filter_vector.append(filter_text)
    return filter_vector


def analyzeSentence(oracion,commonWords):
    # Obtiene las palabras mas relevantes de una sentencia

    # Procesar la oración con el modelo cargado
    doc = nlp(oracion)
    # Filtrar palabras irrelevantes (stop words)
    leaked_words = [token.lemma_.lower(
    ) for token in doc if not token.is_stop and not token.is_punct]
    leaked_words = _filterVector(leaked_words)
    # Calcular la frecuencia de las palabras
    frequency = FreqDist(leaked_words)
    # Obtener las palabras más relevantes
    relevant_words = [word for word,
                           _ in frequency.most_common(commonWords)]
    return relevant_words


def anlizeSimilitary(texto, grupo): # Creo que no lo uso
    doc_texto = nlp(texto)
    doc_descripcion = nlp(grupo)

    similitud = doc_texto.similarity(doc_descripcion)
    return similitud
    # # Establece un umbral de similitud para considerar que la descripción pertenece al texto
    # umbral_similitud = 0.8

    # if similitud > umbral_similitud:
    #     return True
    # else:
    #     return False



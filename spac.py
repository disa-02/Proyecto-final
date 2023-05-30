import spacy


def text(texto):
    # Cargar el modelo de spaCy en español
    nlp = spacy.load('es_core_news_sm')

    # Texto de ejemplo
    # texto = "Este es un ejemplo de texto donde queremos extraer las palabras más relevantes."

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

from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess

# Paso 1: Preprocesamiento de los documentos
documents = ["Este es el primer documento.",
             "Este documento habla sobre tópicos de extracción.",
             "El tercer documento es otro ejemplo."]

# Tokenización y limpieza básica de los documentos
tokenized_docs = [simple_preprocess(doc) for doc in documents]

# Paso 2: Creación del diccionario y la bolsa de palabras
dictionary = corpora.Dictionary(tokenized_docs)
bow_corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

# Paso 3: Entrenamiento del modelo LDA
lda_model = LdaModel(bow_corpus, num_topics=2, id2word=dictionary, passes=10)

# Paso 4: Extracción de tópicos para un documento nuevo
new_doc = "Este es un documento nuevo sobre tópicos de extracción"
new_doc_tokens = simple_preprocess(new_doc)
new_doc_bow = dictionary.doc2bow(new_doc_tokens)

topic_distribution = lda_model.get_document_topics(new_doc_bow)

# Paso 5: Mostrar los tópicos y su distribución
for topic in topic_distribution:
    topic_id = topic[0]
    topic_prob = topic[1]
    topic_keywords = lda_model.show_topic(topic_id)

    print("Tópico {}: {}".format(topic_id, topic_prob))
    print("Palabras clave:")
    for keyword, prob in topic_keywords:
        print("- {} (probabilidad: {})".format(keyword, prob))
    print()

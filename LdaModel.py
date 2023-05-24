from gensim import corpora
from gensim.models import LdaModel

# Lista de listas de palabras
documentos = [
    ['Description', 'generated', 'chatGPT'],
    ['Add', 'new', 'pet', 'the', 'store'],
    ['Multiple', 'status', 'values', 'be',
        'provided', 'comma', 'separated', 'strings'],
    ['Multiple', 'tags', 'be', 'provided', 'comma', 'separated', 'strings',
        '.', 'Use', 'tag1', ',', 'tag2', ',', 'tag3', 'testing', '.'],
    ['Returns', 'single', 'pet'],
    ['Description', 'generated', 'chatGPT'],
    ['delete', 'pet'],
    ['Description', 'generated', 'chatGPT'],
    ['Returns', 'map', 'status', 'codes', 'quantities'],
    ['Place', 'new', 'order', 'the', 'store'],
    ['For', 'valid', 'response', 'try', 'integer', 'IDs', 'value', '<', '=',
        '5', '>', '10', '.', 'Other', 'values', 'generate', 'exceptions', '.'],
    ['For', 'valid', 'response', 'try', 'integer', 'IDs', 'value', '<', '1000',
        '.', 'Anything', '1000', 'nonintegers', 'generate', 'API', 'errors'],
    ['This', 'only', 'done', 'the', 'logged', 'user', '.'],
    ['Creates', 'list', 'users', 'given', 'input', 'array'],
    ['Description', 'generated', 'chatGPT'],
    ['Description', 'generated', 'chatGPT'],
    ['Description', 'generated', 'chatGPT'],
    ['This', 'only', 'done', 'the', 'logged', 'user', '.'],
    ['This', 'only', 'done', 'the', 'logged', 'user', '.']
]

# Crear el diccionario de palabras
diccionario = corpora.Dictionary(documentos)

# Crear la representación de los documentos en forma de bolsa de palabras (bag of words)
corpus = [diccionario.doc2bow(doc) for doc in documentos]

# Entrenar el modelo LDA
num_topics = 4  # Número de tópicos esperados
lda_model = LdaModel(corpus, num_topics=num_topics,
                     id2word=diccionario, passes=10)

# Obtener los tópicos y sus palabras clave
topics = lda_model.print_topics(num_topics=num_topics)
for topic in topics:
    print(topic)

for i, doc in enumerate(corpus):
    topics = lda_model.get_document_topics(doc)
    print(f"Documento {i+1}:")
    for topic in topics:
        print(f"Tópico {topic[0]}: {topic[1]}")
    print()

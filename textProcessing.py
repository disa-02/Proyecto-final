import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


descriptions = {}
pathInfo = {}


def _extractDescriptions(data):
    paths = data.get("paths", {})
    for path, endpoint in paths.items():
        infoDescriptions = {}
        methodInfo = {}
        for method, info in endpoint.items():
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


def procces(data):
    nltk.download('stopwords')
    nltk.download('punkt')
    _extractDescriptions(data)
    _completeDescriptions()
    # for path, endpoint in descriptions.items():
    #     for method, description in endpoint.items():
    #         print(description)
    _delStopWords()
    for path, endpoint in descriptions.items():
        for method, description in endpoint.items():
            print(description)
    _joinDescriptions()
    return descriptions

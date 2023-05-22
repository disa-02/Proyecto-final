import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class textProcessing:

    def __init__(self):
        self.descriptions = {}
        self.pathInfo = {}

    def _extractDescriptions(self, data):
        paths = data.get("paths", {})
        for path, endpoint in paths.items():
            infoDescriptions = {}
            methodInfo = {}
            for method, info in endpoint.items():
                description = info.get("description")
                infoDescriptions[method] = description
                if (description == None or description == ''):
                    methodInfo[method] = info.items()
                    self.pathInfo[path] = methodInfo
            self.descriptions[path] = infoDescriptions

    def _completeDescriptions(self):
        for path, endpoint in self.pathInfo.items():
            for method, description in endpoint.items():
                # desc = request to chatGPT
                desc = "Description generated with chatGPT"
                self.descriptions[path][method] = desc

    def _delStopWords(self):
        for path, endpoint in self.descriptions.items():
            for method, description in endpoint.items():
                if (description != None):
                    # Tokenizacion
                    text = word_tokenize(description)
                    # Eliminacion de las stopWords
                    for word in text:
                        if (word in stopwords.words('english')):
                            text.remove(word)
                self.descriptions[path][method] = text

    def _joinDescriptions(self):
        for path, endpoint in self.descriptions.items():
            for method, description in endpoint.items():
                description = ' '.join(description)
                self.descriptions[path][method] = description

    def procces(self, data):
        nltk.download('stopwords')
        nltk.download('punkt')
        self._extractDescriptions(data)
        self._completeDescriptions()
        # for path, endpoint in self.descriptions.items():
        #     for method, description in endpoint.items():
        #         print(description)
        self._delStopWords()
        self._joinDescriptions()
        return self.descriptions



class textProcessing:

    def __init__(self, stopWords):
        self.descriptions = {}
        self.pathInfo = {}
        self.stopWords = stopWords

    def _extractDescriptions(self, data):
        paths = data.get("paths", {})
        # descriptions = {}  # Almacena las descripciones de los metodos
        # pathInfo = {}  # Almacena todos los items de los metodos que no tienen informacion
        for path, endpoint in paths.items():
            infoDescriptions = {}
            methodInfo = {}
            for method, info in endpoint.items():
                description = info.get("description")
                infoDescriptions[method] = description
                if (description == None):
                    methodInfo[method] = info.items()
                    self.pathInfo[path] = methodInfo
            self.descriptions[path] = infoDescriptions
        # return descriptions, pathInfo

    def _completeDescriptions(self):
        for path, endpoint in self.pathInfo.items():
            for method, description in endpoint.items():
                # desc = request to chatGPT
                desc = "Description generated with chatGPT"
                self.descriptions[path][method] = desc

    def _delStopWords(self):
        for path, endpoint in self.descriptions.items():
            for method, description in endpoint.items():
                desc = ''
                if (description != None):
                    for word in description.split(' '):
                        if (word not in self.stopWords):
                            desc += word + ' '
            self.descriptions[path][method] = desc

    def procces(self, data):
        self._extractDescriptions(data)
        print(self.descriptions)
        print()
        print(self.pathInfo)
        self._completeDescriptions()
        self._delStopWords()
        print()
        print(self.descriptions)

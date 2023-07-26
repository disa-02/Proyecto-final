class OpenApiFile:

    def __init__(self,name,data):
        self.name = name
        self.data = data
        self.methods = []
        self.groups = []
        self.vectorGroups = []

    def __str__(self):
        return self.name

    def getData():
        return self.data
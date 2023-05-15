from textProcessing import textProcessing

import yaml


def fileImport(fileName):
    try:
        file = open(fileName, 'r')
        data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print("The file does not exists")
    return None


stopWords = ["new"]
data = fileImport("openapi.yaml")
x = textProcessing(stopWords)
x.procces(data)

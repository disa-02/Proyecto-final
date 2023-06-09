import yaml
import os


def _fileImport(fileName):
    try:
        file = open(fileName, 'r')
        data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print("The file does not exists")
    return None


def filesImport(folderDir):
    files = os.listdir(folderDir)
    fileList = []
    # Imprimir los nombres de los archivos
    for fileName in files:
        # chequear si es .yaml
        # print(fileName)
        data = _fileImport(folderDir + "/" + fileName)
        # print(data)
        fileList.append(data)
    return fileList


def saveFile(text, name, dir, mode):
    newFile = open(dir + name, mode)
    newFile.write(text)
    newFile.close()


def deleteFile(path):
    if (os.path.exists(path)):
        os.remove(path)

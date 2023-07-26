import yaml
import os


def _fileImport(fileName):
    # Importa un archivo de tipo yaml
    try:
        file = open(fileName, 'r')
        data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print("The file does not exists")
    return None


def filesImport(folderDir):
    # Importa todos los archivos yaml de una carpeta
    files = os.listdir(folderDir)
    fileList = []
    for fileName in files:
        # chequear si es .yaml
        # print(fileName)
        data = _fileImport(folderDir + "/" + fileName)
        # print(data)
        fileList.append(data)
    return fileList, files


def saveFile(text, name, dir, mode):
    newFile = open(dir + name, mode)
    newFile.write(text)
    newFile.close()


def deleteFile(path):
    if (os.path.exists(path)):
        os.remove(path)

def openTxt(dir):
    # Lee un archivo txt que tiene una lista de "key:valor" separados por salto de linea
    try:
        entries = []    
        with open(dir,"r") as fileTxt:
            content = fileTxt.read()
            content = content.split("\n")
            for cont in content:
                # if (cont != ""): # Tengo en cuenta lineas vacias
                cont = cont.split(":")
                if(len(cont) == 2):
                    entries.append(cont[1])
        return entries
    except FileNotFoundError:
        print(f"El archivo de entrada no se encontró.")
    except IOError:
        print(f"Ocurrió un error al intentar leer el archivo.")
    except IndexError:
        print(f"El archivo de entrada se encuentra mal definido.")
        

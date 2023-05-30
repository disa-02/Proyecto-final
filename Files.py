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


def saveFile(text, name, dir):
    newFile = open(dir + name, "w")
    newFile.write(text)
    newFile.close()


filesImport("./openApiDescriptions")

text = "{'task management': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 79, 82, 83, 103, 104, 105, 107, 108, 113, 114, 115, 116, 121, 123, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 328, 329, 330, 344, 342, 343, 345, 322, 323, 324, 325, 326, 327, 335, 336, 337, 338, 339, 342, 346], 'goals': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], 'project management': [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 62, 67, 69, 70, 72, 73, 74, 76, 77, 78, 80, 81, 285, 286, 287, 288, 289, 290, 291, 294, 295, 296, 297, 352, 353, 354, 355, 364, 378, 381, 382, 385], 'team management': [123, 124, 125, 126, 127, 132, 133, 287, 291, 352, 356, 366], 'user management': [88, 89, 90, 91, 139, 140, 141, 144, 312, 362, 363, 367, 383, 426, 437, 441, 443, 444, 445], 'tag management': [92, 94, 95, 96, 97, 315, 317, 318, 319, 320, 345, 384, 385], 'portfolio management': [32, 33, 35, 36, 37, 39, 43, 44, 45, 46], 'attachment management': [1, 2, 3, 4, 225, 226, 227, 228, 229], 'custom field management': [6, 7, 8, 9, 10, 230, 231, 232, 233, 235, 285, 289, 294], 'subscription and export': [13, 30, 31, 254, 255, 380], 'record management': [14, 15, 16, 17, 19, 20, 21, 24, 28, 38, 50, 53, 54, 55, 56, 62, 68, 72, 88, 90, 91, 98, 101, 102, 120, 128, 146, 149, 156, 168, 175, 178, 179, 180, 186, 188, 196, 200, 201, 203, 204, 219, 222, 279, 283, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 311, 313, 314, 336, 340, 341, 342, 343, 344, 345, 363, 365, 367, 369, 374, 375, 376, 377, 382, 383, 388, 390, 436], 'blockchain management': [172, 178, 182, 184, 187, 189, 190, 193, 196, 198, 199, 204, 206, 207, 208, 210, 211, 212, 214, 215, 218, 405, 407, 410, 416, 419, 421, 427, 433], 'new group': [295, 296, 303, 306, 307, 311, 314, 345, 376, 381, 382, 384, 433, 435]}"

saveFile(text, "prueba.py", "./outs/")

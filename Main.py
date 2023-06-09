import textProcessing
import ChatGPTChunks
import Files
from tqdm import tqdm


# Importacion de los documentos
data = Files.filesImport("./openApiDescriptions")
descriptions = []

# Procesamiento de los documentos
print("\nProcesando documentos:")
for d in tqdm(data, desc="Documento"):
    descriptions.append(textProcessing.procces(d))

# Obtencion de las descripciones como una lista enumerada
lista = []
cont = 1
for description in descriptions:
    for path, endpoint in description.items():
        for method, description in endpoint.items():
            lista.append('' + str(cont) + "-" + description)
            cont += 1
Files.saveFile("\n".join(lista), "DescripcionesProcesadas.txt", "./outs/", "w")

# Consultas al chatGpt
respuesta = ChatGPTChunks.agrupar(lista)
Files.saveFile(
    str(respuesta), "AgrupacionDeDescripciones.json", "./outs/", "w")

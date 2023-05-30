import textProcessing
import ChatGPTChunks
import Files
from tqdm import tqdm


data = Files.filesImport("./openApiDescriptions")
descriptions = []
print("\nProcesando documentos:")
for d in tqdm(data, desc="Documento"):
    descriptions.append(textProcessing.procces(d))
lista = []
cont = 1
for description in descriptions:
    for path, endpoint in description.items():
        for method, description in endpoint.items():
            lista.append('' + str(cont) + "-" + description)
            cont += 1
# respuesta = ChatGPTChunks.agrupar(lista)
Files.saveFile(str(respuesta), "AgrupacionDeDescripciones.json", "./outs/")

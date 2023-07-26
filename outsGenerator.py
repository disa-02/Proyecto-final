
def generateOutFiles(filesDescriptions,vectorGroups):
    outs = []
    cont = 0
    for openApiFile in filesDescriptions:
        out = ""
        contDesc = 0
        for path, endpoint in openApiFile.items():
            out = out + str(path) + ":\n"
            for method, description in endpoint.items():
                out = out + "  " + str(method) + ":\n"
                out = out + "    " + "Descripcion: " + str(description) + "\n"
                out = out + "    " + "Vector de grupo: " + str(vectorGroups[cont][contDesc]) + "\n"
                contDesc = contDesc + 1
        outs.append(out)
        cont = cont + 1
    return outs

def generateOutVectorization(res,filesNames):
    # Genera la salida del resultado de vectorizar los documentos
    out = ""
    for i in range(0,len(res)):
        out = out + str(filesNames[i]) + ": " + str(res[i]) + "\n"
    return out

def generateOutCluster(data,sse,centroids,k,filesNames):
    # Genera la salida del resultado de aplicar clustering sobre los documentos,es la salida final del programa
    out = ""
    for i in range(0,k):#k
        out = out + "Group " + str(i) + ":\n"
        for num in range(0,len(data)):
            if(data[num] == i):
                out = out + str(filesNames[num]) + "\n"
        out = out + "\n"
    out = out + "\n"
    out = out + "SSE: " + str(sse) + "\n\n"
    out = out + "Centroides: \n" + str(centroids)
    return out
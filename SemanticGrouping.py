import spac

def group(enumFilesDescriptions,umbral):
    groups = {}
    key = 0
    visited = [0] * len(enumFilesDescriptions)
    for i in range(len(enumFilesDescriptions)):
        if(visited[i] == 0):
            description = enumFilesDescriptions[i]
            groups[key] = [i]
            visited[i] = 1
            for j in range (i + 1,len(enumFilesDescriptions)):
                if(visited[j] == 0):
                    comparedDescritpion = enumFilesDescriptions[j]
                    similitary = spac.anlizeSimilitary(description, comparedDescritpion)
                    if(similitary > umbral):
                        groups[key].append(j)
                        visited[j] = 1
            key = key + 1

    return groups

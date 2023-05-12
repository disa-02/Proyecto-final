import yaml

def fileImport(fileName):
    try:
        file = open(fileName,'r')
        data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print("The file does not exists")
    return None
    
def extractDescriptions(data):   
    paths = data.get("paths",{})
    descriptions = {} #Almacena las descripciones de los metodos
    pathInfo = {} #Almacena todos los items de los metodos que no tienen informacion
    for path,endpoint in paths.items():
        infoDescriptions = {} 
        methodInfo = {}
        for method,info in endpoint.items():
            description = info.get("description")
            infoDescriptions[method] = description
            if(description == None):
                methodInfo[method] = info.items()
                pathInfo[path] = methodInfo                
        descriptions[path] = infoDescriptions
    return descriptions, pathInfo  
    
data = fileImport("openapi.yaml")
descriptions, pathInfo = extractDescriptions(data)
print(descriptions)
print()
print(pathInfo)
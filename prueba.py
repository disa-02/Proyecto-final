import json
import collections

# Convertir el string en un objeto JSON
json_string = "{"
json_string += "  \"a\": [1,2,3],"
json_string += "  \"b\": [4,4,5],"
json_string += "  \"c\": [4,2,4],"
json_string += "  \"d\": [2,4,1]"
json_string += "}"


def _checkRepeatedTopics(response):
    repeated = set()
    dic = json.loads(response)
    for key in dic:
        valores = dic[key].copy()
        i = 0
        for valor in valores:
            if valor in repeated:
                del dic[key][i]
            else:
                i = i+1
                repeated.add(valor)
    return json.dumps(dic)

final = _checkRepeatedTopics(json_string)
print(final)
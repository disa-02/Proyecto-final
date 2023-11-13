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

    return groups, -5

words = ["0-accounts", "1-acounts", "2-autopilot", "3-bulkexport", "4-chat", "5-chat", "6-content", "7-conversation", "8-events", "9-fax", "10-flex", "11-flex", "12-frontline", "13-insights", "14-main topic", "15-intelligence", "16-ip", "17-ip", "18-lookups", "19-lookups", "20-media", "21-messaging", "22-microvisor", "23-monitor", "24-notify", "25-numbers", "26-auth", "27-preview", "28-pricing", "29-proxy", "30-routes", "31-serverless", "32-studio", "33-studio", "34-supersim", "35-sync", "36-taskrouter", "37-trunking", "38-trusthub", "39-verify", "40-video", "41-voice", "42-wireless"]
groups = group(words,0.82)
print(groups)
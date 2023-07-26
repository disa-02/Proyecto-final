import openai
import Files
# Obtener la clave de API de OpenAI
api_key = str(Files.openTxt("./entries.txt")[6])


# Crear un objeto ChatGPT
chatgpt = openai.Client(api_key)

# Generar un conjunto de datos de texto
text_data = [
  "El gato está sentado en la mesa.",
  "El perro está ladrando en el parque.",
  "El pájaro está volando en el cielo.",
  "El pez está nadando en el agua.",
  "La flor está floreciendo en el jardín."
]

# Entrenar el modelo `davinci` en el conjunto de datos de texto
chatgpt.train(text_data)

# Utilizar el modelo `davinci` para agrupar el texto
clusters = chatgpt.cluster(text_data)

# Imprimir los grupos
# for cluster in clusters:
#   name = chatgpt.generate(prompt="Dame un nombre para este grupo: {}".format(cluster))
#   print(cluster, name)
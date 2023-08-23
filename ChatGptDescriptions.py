import openai
import time
import Files

language = model = str(Files.openTxt("./entries.txt")[11])

statement = "Dado el siguiente endpoint perteneciente a un archivo de openApi, generar una descripcion que explique resumidamente la funcionalidad del endpoint. Se debe generar en una unica oracion en el idioma " + language + ": "


def consult(prompt):
    # Realiza una consulta al chat gpt para generar una descripcion de un endpoint 
    condition = True
    response = ''
    while (condition):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ])
            response = (completion.choices[0].message.content)
            condition = False
        except openai.error.RateLimitError as error:
            print("Error de tiempo al generar descripcion, reintentando...")
            time.sleep(65)
        except openai.error.ServiceUnavailableError as e:
            print("Error: El servidor está sobrecargado o no está listo todavía, reintentando...")
            time.sleep(65)
        except Exception as e:
            print("Posible error de tiempo, reintentando en 1 minuto ...")
            time.sleep(65)
    return response


def generateDescription(endpoint):
    # Genera la descripcion de un endpoint
    prompt = statement + str(endpoint)
    response = consult(prompt)
    return response

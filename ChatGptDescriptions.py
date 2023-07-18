import openai
import time

enunciado = "Dado el siguiente endpoint perteneciente a un archivo de openApi, generar una descripcion que explique resumidamente la funcionalidad del endpoint. Se debe generar en una unica oracion: "


def consultar(prompt):
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
            time.sleep(5)
        except openai.error.ServiceUnavailableError as e:
            print("Error: El servidor está sobrecargado o no está listo todavía, reintentando...")
            time.sleep(5)
    return response


def generateDescription(endpoint):
    prompt = enunciado + str(endpoint)
    response = consultar(prompt)
    return response

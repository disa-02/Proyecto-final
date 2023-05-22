import os
import openai


class ChatGPT:

    def __init__(self):
        pass

    def agrupar(self, lista):
        openai.api_key = "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"
        prompt = """Dado los siguientes temas. Agrupa sus elementos según su relación semántica. 
                    Los temas no pueden pertenecer a mas de un grupo. 
                    Dar la respuesta en un json  donde cada atributo sea el nombre de grupo y el valor una lista de los temas. 
                    El nombre de grupo debe ser representativo a los temas que agrupa. 
                    La lista de temas debe ser unicamente numerica y cada numero debe corresponder al 
                    identificador de cada tema, no debe haber strings en este atributo.
                    Lista de temas:  """.join(lista)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ])
        print('Respuesta')
        print("\n")
        print(completion.choices[0].message.content)
        print(("\n"))

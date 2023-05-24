import os
import openai


def agrupar(lista):
    openai.api_key = "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"
    prompt = """Dado los siguientes temas. Agrupa sus elementos según su relación semántica. 
                Los temas no pueden pertenecer a mas de un grupo. 
                Dar la respuesta en un json  donde cada atributo sea el nombre de grupo y el valor una lista de los temas. 
                El nombre de grupo debe ser representativo a los temas que agrupa. 
                La lista de temas debe ser unicamente numerica y cada numero debe corresponder al 
                identificador de cada tema, no debe haber strings en este atributo.
                Intenta que en las agrupaciones no queden grupos con un unico tema.
                Lista de temas:  """ + " ".join(["".join(text) for text in lista])
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ])
    return completion.choices[0].message.content

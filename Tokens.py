import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
assert enc.decode(enc.encode("hello world")) == "hello world"

# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4")
print(enc)


# def contar_tokens(texto):
#     tokens = tiktoken.count_tokens(texto)
#     return tokens


# contar_tokens("textholao")

# def dividir_por_tokens(texto, max_tokens):
#     tokenizer = Tokenizer()
#     tokens = tokenizer.tokenize(texto)
#     partes = []
#     parte_actual = ""
#     tokens_actuales = 0

#     for token in tokens:
#         if tokens_actuales + token['num_tokens'] <= max_tokens:
#             parte_actual += token['token']
#             tokens_actuales += token['num_tokens']
#         else:
#             partes.append(parte_actual)
#             parte_actual = token['token']
#             tokens_actuales = token['num_tokens']

#     partes.append(parte_actual)  # Agregar la última parte

#     return partes

vector = [1, 2]
vec = [1, 2, 3]

cont = 0
numeros = []
for v in vector:
    nums = []
    for a in vec:
        nums.append(cont)
        cont = cont + 1
    numeros.append(nums)

print(numeros)

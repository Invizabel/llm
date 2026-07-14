import ast
import collections
import random
import re

# https://www.reddit.com/r/todayilearned/comments/dwvm1k/til_that_the_average_length_of_a_word_in_the/
max_token_size = 5

context_tokens = 4

def tokenizer(data):
    out = []
    for i in range(1,max_token_size+1):
        tokens = re.findall(".{" + str(i) + "}", data)
        for token in tokens:
            out.append(token)
    return out

def bubble(data):
    out = []
    for i in range(len(data)):
        out.append(data[i:i+context_tokens])
    return out

def collapse(data,precision=9):
    data = collections.Counter(tuple(i) for i in data)
    n = len(data)
    out = [[list(key), round(value / n, precision)] for key, value in data.items()]
    return out
            
def Train():
    with open("bible.txt", "r") as file:
        data = file.read()

    # tokenize it
    print("tokenizer")
    data = tokenizer(data)

    # bubble it (groupings)
    print("bubble")
    data = bubble(data)

    # collapse it (find # of occurences)
    print("collapse")
    data = collapse(data)
    with open("model.txt", "w") as file:
        for i in data:
            file.write(f"{i}\n")

def Test():
    data = []
    with open("model.txt") as file:
        for line in file:
            if line.strip():  # skip empty lines
                data.append(ast.literal_eval(line.strip()))

    values = [x[0] for x in data]
    weights = [x[1] for x in data]
    result = random.choices(values, weights = weights, k = 1024)

    for i in result:
        print("".join(i), end = "", flush = True)

Test()
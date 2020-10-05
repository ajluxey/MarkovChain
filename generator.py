from funcs import markov_chain
from random import random
from time import time


cdf = None


def get_symbol(table):
    rnd = random()
    for key in table:
        if rnd < table[key]:
            return key


def round_table(table, generated):
    if not generated:
        return table
    else:
        key = generated[0]
        if key in table:
            return round_table(table[key], generated[1:])
        else:
            return


def generate_symbol(generated, index):
    global cdf
    while True:
        answer = round_table(cdf[index], generated)
        if answer:
            return get_symbol(answer)
        else:
            generated = generated[1:]
            index -= 1


def generator(n):
    global cdf

    depth = len(cdf)
    string = ''
    for i in range(1, n+1):
        index = i if i <= depth else depth
        string += generate_symbol(string[-index+1:], index)
    return string


def main():
    global cdf
    _, _, cdf = markov_chain(r'.\src', 8)
    while True:
        print(generator(100))
        if input():
            break


if __name__ == '__main__':
    main()

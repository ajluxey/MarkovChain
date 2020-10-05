import sys
import os
from os import path
from collections import Counter
from pprint import pprint
from time import time


# def count_freq(collection, table):
#     if len(collection) > 1:
#         if collection[0] not in table:
#             if len(collection) == 2:
#                 new_table = Counter()
#             else:
#                 new_table = dict()
#             table.setdefault(collection[0], new_table)
#         count_freq(collection[1:], table[collection[0]])
#     else:
#         table[collection] += 1


def count_freq(collection, table):
    l = len(collection)
    for num, el in enumerate(collection[:-1]):
        if el not in table:
            if num - l + 2 == 0:
                table[el] = Counter()
            else:
                table[el] = dict()
        table = table[el]
    table[collection[-1]] += 1


# def create_statistics(tables):
#     stats = {}
#     for key in tables:
#         stats.setdefault(key, {})
#         fill_stats(tables[key], stats[key])
#     return stats
#
#
# def fill_stats(table, stats):
#     for key in table:
#         if isinstance(table[key], dict):
#             stats.setdefault(key, dict())
#             fill_stats(table[key], stats[key])
#         else:
#             break
#     else:
#         return
#     amount = sum(list(table.values()))
#     for key in table:
#         stats[key] = table[key]/amount


def new_table(func):
    def wrapper(tables):
        return round_and_creating_new_tables(tables, func)
    return wrapper


# _________ попытаться объединить в декоратор _________
def round_and_creating_new_tables(tables, func):
    new_tables = {}
    for key in tables:
        new_tables.setdefault(key, {})
        fill_tables(tables[key], new_tables[key], func)
    return new_tables


def fill_tables(tables, new_tables, fill_func):
    for key in tables:
        if isinstance(tables[key], dict):
            new_tables.setdefault(key, dict())
            fill_tables(tables[key], new_tables[key], fill_func)
        else:
            break
    else:
        return
    fill_func(tables, new_tables)
# _________ попытаться объединить в декоратор _________


@new_table
def stats_filling(table, stats):
    amount = sum(list(table.values()))
    for key in table:
        stats[key] = table[key]/amount


@new_table
def CDF_filling(table, cdf):
    prev = 0
    for key in table:
        cdf.setdefault(key, table[key] + prev)
        prev = cdf[key]


def filling(collection, tables):
    for index in range(1, len(collection)+1):
        count_freq(collection[:index], tables[index])


def filling_by_files(src, depth):
    files = get_files(src)
    for file in files:
        text = ''
        for c in read_text(path.join(src, file), depth):
            text = text[1:] + c
            yield text
        # прокручиваем хвост
        for i in range(1, len(text)):
            text = text[1:]
            yield text


def get_files(src):
    src = path.abspath(src)

    if not path.exists(src):
        raise FileNotFoundError('Directory doesn\'t exist')

    if not path.isdir(src):
        raise NotADirectoryError('Src is a directory path with files')

    files = os.listdir(src)
    if not files:
        raise FileNotFoundError('Directory doesn\'t have any files')
    else:
        return files


def markov_chain(src, depth=None):
    if not depth:
        depth = int(input('depth of chain?\n>>> '))

    tables = dict()
    tables[1] = Counter()
    for i in range(2, depth+1):
        tables.setdefault(i, dict())

    for collection in filling_by_files(src, depth):
        filling(collection, tables)

    stats = stats_filling(tables)
    cdf = CDF_filling(stats)

    # stats = round_and_creating_new_tables(tables, stats_filling)
    # cdf = round_and_creating_new_tables(stats, CDF_filling)
    return tables, stats, cdf


def read_text(file, depth):
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read(depth)
        while c:
            yield c
            c = f.read(1)


if __name__ == '__main__':
    _, _, cdf = markov_chain(r'.\src', 2)
    # print(cdf)
    # if len(sys.argv) == 1:
    #     markov_chain(r'.\src')

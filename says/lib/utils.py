# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


def filter_gt(seq, thresh=1):
    return  dict( (i, val) for i, val in seq.items() if val >= thresh )


def getid(table, key):
    try:
        id = table[key]
    except KeyError:
        table[key] = len(table)+1
        id = table[key]
    return id


def count(table, key):
    try:
        table[key] += 1
    except KeyError:
        table[key] = 1


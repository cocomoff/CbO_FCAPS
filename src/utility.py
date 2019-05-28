# -*- coding: utf-8 -*-

def set2str(S):
    if len(S) == 0:
        return "{}"
    s = "{"
    for v in S:
        s += ("%d," % v)
    s = s[:-1] + "}"
    return s

def counter2str(C):
    if len(C) == 0:
        return "{}"
    s = "{"
    for v in C:
        for x in xrange(C[v]):
            s += ("%d " % v)
        s = s[:-1] + ","
    s = s[:-1] + "}"
    return s

def se(p, n):
    from math import log
    all = p+n
    return -p * log(1.0 + 1.0*p/all, 2) - n * log(1.0 + 1.0*n/all, 2)
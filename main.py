# -*- coding: utf-8 -*-

from src.cbo import *
from src.cbop import IntervalPatternStructure, ClosedByOnePattern
from src.data_structure import Interval, Intervals
from math import sqrt
from itertools import product

def example_fca():
    o_all = [1, 2, 3, 4, 5]
    a_all = [1, 2, 3, 4]
    rel = [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (4, 1), (4, 2), (4, 4), (5, 4)]
    ct = Context(rel, o_all, a_all)
    alg = ClosedByOne(ct)
    set_of_concepts = alg.close_by_one()

    for p in set_of_concepts:
        print(p)

def convert(lov):
    ret = []
    for idx, l in enumerate(lov):
        ll = []
        for value in l:
            ll.append(Interval(value, value))
        ret.append((idx, Intervals(ll)))
    return ret

def example_ps():
    db_raw = [[1, 5, 1], [2, 7, 1], [3, 6, 1], [3, 5, 5], [5, 6, 5]]
    db = convert(db_raw)
    print("database")
    print("\n".join(map(lambda x: "{}:{}".format(x[0], str(x[1])), db)))
    print()
    ps = IntervalPatternStructure(db)
    alg = ClosedByOnePattern(ps)
    set_of_concepts = alg.close_by_one()

    for pc in set_of_concepts:
        print(pc)

    print()
    print("in total: {}".format(len(set_of_concepts)))

    # compute L1
    for pc in set_of_concepts:
        A = pc.intent
        if A != set({1, 2}) and A != set({0, 1, 2}) and A != set({3, 4}):
            continue
        diff = 0
        for i, j in product(A, A):
            if i == j:
                continue

            gid = ps.square_(i)
            gjd = ps.square_(j)
            diffIJ = 0
            for k in range(gid.dim):
                diffIJ += (gid.intervals[k].left - gjd.intervals[k].left) ** 2
            diffIJ = sqrt(diffIJ)
            diff += diffIJ
            print("  ", i, j, diffIJ)
            print("      ", i, gid)
            print("      ", j, gjd)
            for k in range(gid.dim):
                print("      ", k, gid.intervals[k], gjd.intervals[k])
        diff /= (len(A) * len(A))
        print(A, diff, pc.extent)

if __name__ == '__main__':
    example_ps()
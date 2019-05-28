# -*- coding: utf-8 -*-

from src.cbo import *
from src.cbop import IntervalPatternStructure, ClosedByOnePattern
from src.data_structure import Interval, Intervals

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

if __name__ == '__main__':
    example_ps()
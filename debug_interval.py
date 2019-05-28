# -*- coding: utf-8 -*-

from src.cbop import *
from src.data_structure import Interval, Intervals

def example_interval():
    int1 = Interval(1, 2)
    int2 = Interval(3, 4)
    int3 = Interval(2, 3)
    int12 = int1.meet(int2)
    int13 = int1.meet(int3)
    int23 = int2.meet(int3)
    int123 = int12.meet(int3)
    print(int1)
    print(int2)
    print(int3)
    print(int12)
    print(int13)
    print(int23)
    print(int123)

def example_intervals():
    itv1 = Intervals([Interval(1, 1), Interval(5, 5), Interval(1, 1)])
    itv2 = Intervals([Interval(2, 2), Interval(7, 7), Interval(1, 1)])
    itv3 = Intervals([Interval(3, 3), Interval(6, 6), Interval(1, 1)])
    itv12 = itv1.meet(itv2)
    itv13 = itv1.meet(itv3)
    itv23 = itv2.meet(itv3)
    itv123 = itv12.meet(itv3)
    print(itv1)
    print(itv2)
    print(itv3)
    print(itv12)
    print(itv13)
    print(itv23)
    print(itv123)

if __name__ == '__main__':
    example_intervals()
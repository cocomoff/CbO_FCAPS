# -*- coding: utf-8 -*- 

import os
import pickle
from .utility import set2str, counter2str
from collections import defaultdict

class Interval(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hash_value = hash(left) ^ hash(right)

    """ Pickle """
    def __getstate__(self): 
        return self.__dict__
    def __setstate__(self, state): 
        self.__dict__.update(state)
    def __reduce__(self):
        return (self.__class__, (self.left, self.right))

    """ Length """
    def __len__(self):
        return self.right - self.left + 1

    """ Print """
    def __str__(self):
        return "[%s,%s]" % (self.left, self.right)

    def __eq__(self, that):
        return self.left == that.left and self.right == that.right

    def get_description(self):
        return self

    """ Hash """
    def __hash__(self):
        return self.hash_value

    """ size """
    def size(self):
        return self.__len__()

    """ Common part operation (\sqcap) """
    def meet(self, t2, debug_print = False):
        ll = min(self.left, t2.left)
        rr = max(self.right, t2.right)
        return Interval(ll, rr)

    def is_generalized(self, t2):
        t12 = self.meet(t2)
        return self.left == t12.left and self.right == t12.right

class Intervals(object):
    def __init__(self, intervals):
        self.intervals = intervals
        self.dim = len(intervals)

    """ Pickle """
    def __getstate__(self): 
        return self.__dict__
    def __setstate__(self, state): 
        self.__dict__.update(state)
    def __reduce__(self):
        return (self.__class__, (self.intervals))

    """ Length """
    def __len__(self):
        return self.dim

    """ Print """
    def __str__(self):
        s = ",".join(map(lambda x: str(x), self.intervals))
        return "<{}>".format(s)
 
    """ Equivalency """
    def __eq__(self, that):
        return self.intervals == that.intervals

    """ Hash """
    def __hash__(self):
        hash_value = hash(self.intervals[0])
        for itv in self.intervals[1:]:
            hash_value = hash_value ^ hash(itv)
        return hash_value

    def get_description(self):
        return self

    """ size """
    def size(self):
        return self.__len__()

    """ Common part operation (\sqcap) """
    def meet(self, t2, debug_print = False):
        if self.dim != t2.dim:
            raise AssertionError("Dimension missmatch")
        list_of_itvs = [self.intervals[i].meet(t2.intervals[i]) for i in range(self.dim)]
        return Intervals(list_of_itvs)

    def is_generalized(self, t2):
        t12 = self.meet(t2)
        return self.intervals == t2.intervals


### PSA: pattern concept (X, d)
class PatternConcept(object):
    def __init__(self, X, Y, parent, id):
        self.intent = X
        self.extent = Y
        self.parent = parent
        self.id     = id
        self.lenI = len(X)
        self.lenE = len(Y)
        self.flag1 = True

    """ Pickle """
    def __getstate__(self):
        return self.__dict__
    def __setstate__(self, state):
        self.__dict__.update(state)
    def recover(tp): 
        it, et, pa, id = tp
        return PatternConcept(it, et, pa, id)
    def __reduce__(self):
        return (self.__class__, (self.intent, self.extent, self.parent, self.id))

    """ set """
    def __len__(self):
        return self.lenI + self.lenE

    def __hash__(self):
        if self.lenI == 0 and self.lenE == 0:
            return 1
        elif self.lenE == 0:
            return hash(self.lenI)
        elif self.lenI == 0:
            return hash(self.lenE)
        else:
            return hash(list(self.intent)[0])

    def __richcmp__(self, other, tp):
        if tp == 2:
            return self.intent == other.intent and self.extent == other.extent
        else:
            return -1

    def __cmp__(self, other):
        return self.intent == other.intent

    def __str__(self):
        return "[%s, %s]" % (set2str(self.intent), self.extent)

    def content(self):
        return "[%d:%s]" % (len(self.intent), self.extent)

    def extent_str(self):
        return "%s" % self.extent


def compute_edges(L, N, debug_flag = False, bottom_flag = False):
    """
    Input: list of concepts
    Output: edges among concepts
    """
    # DEBUG OUTPUT
    if debug_flag:
        for i in range(len(L)):
            print(" ", i, ": ", set2str(L[i].intent), ", ", L[i].extent)
        print()

    subset_dict = defaultdict(set)
    top = -100
    for i in xrange(len(L)):
        if len(L[i].intent) == N:
            top = i
        for j in xrange(len(L)):
            if i != j:
                if L[i].intent <= L[j].intent:
                    subset_dict[i].add(j)

    ### generate edge map
    all_edge_map = defaultdict(set)
    bottom = len(subset_dict)+1
    for i in xrange(len(L)):
        if i not in subset_dict and i != top:
            all_edge_map[i].add(top)
        elif bottom_flag and len(L[i].intent) == 1:
            all_edge_map[i].add(bottom)
        else:
            candidate = subset_dict[i]
            target    = list(subset_dict[i])
            for j in target:
                if j in subset_dict:
                    candidate -= subset_dict[j]
            all_edge_map[i] = candidate

    if debug_flag:
        print(" -- edges -- ")
        for key in all_edge_map:
            print(" ", key, ": ", all_edge_map[key])
    return all_edge_map
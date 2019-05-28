# -*- coding: utf-8 -*-

import random
import pickle
from operator import itemgetter
from .data_structure import PatternConcept

### P=(G, (D,meet of D), delta)
class IntervalPatternStructure(object):
    """ Initialize """
    def __init__(self, db):
        self.database = db
        self.len_database = len(self.database)

        # memorization of delta
        self.delta_list = list()
        for i in range(self.len_database):
            self.delta_list.append(self.square_(i))

    def size(self): 
        return len(self.database)

    """ Id / Object Transformation """
    def id2obj(self, idx):
        return self.database[idx]

    """ Galois Connection Square: G --> D """
    def square_(self, oelem):
        return self.id2obj(oelem)[1].get_description()

    def square(self, o_set):
        i_tree = None
        for oelem in o_set:
            if i_tree is None:
                i_tree = self.id2obj(oelem)[1].get_description()
            ist = self.id2obj(oelem)[1]
            tt = ist.get_description()
            i_tree = i_tree.meet(tt)
        return i_tree

    """ Galois Connection Diamond: D --> G """
    def diamond(self, dso):
        ans = set()
        for i in range(self.len_database):
            tti = self.id2obj(i)[1].get_description()
            dsom = dso.meet(tti)
            if dsom == dso:
                ans.add(i)
        return ans

class ClosedByOnePattern:
    """ Initialize """
    def __init__(self, ps, dflag = False):
        self.debug_print = dflag
        self.L = list()
        self.ps = ps
        self.N = ps.size()

    """ Entry Point """
    def close_by_one(self):
        for gid in range(self.N):
            set_g_i = {gid}
            fg = self.ps.delta_list[gid]
            gfg = self.ps.diamond(fg)
            self.process(set_g_i, gid, gfg, fg, -1)
        return self.L

    """ Bottom up generation """
    def process(self, Ai, i, Ci, Di, id):
        rset = [h for h in Ci if h not in Ai and h < i]

        if len(rset) == 0 and len(Ci) > 0:
            self.L.append( PatternConcept(Ci, Di, id, len(self.L)) )
            newid = len(self.L) - 1

            fset = [x for x in range(i, self.N) if x not in Ci]
            for j in fset:
                Z = Ci.copy(); Z.add(j)
                F = self.ps.square_(j)
                Y = Di.meet(F)
                X = self.ps.diamond(Y)
                self.process(Z, j, X, Y, newid)
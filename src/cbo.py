# -*- coding:utf-8 -*-

from collections import defaultdict
from .utility import set2str

class Concept(object):
    def __init__(self, X, Y, id=-1):
        self.extent, self.intent = X, Y
        self.id   = id
        self.dics = ",".join(map(str, sorted(Y)))
    def __eq__(self, other):
        return self.intent == other.intent and self.extent == other.extent
    def __str__(self):
        return "({0},{1})".format(set2str(self.extent), set2str(self.intent))
    
class Context(object):
    def __init__(self, relation, o=None, a=None):
        self.relation = relation
        self.o2A = dict()
        self.a2O = dict()
        self.relation_map = defaultdict(set)
        self.relation_inv_map = defaultdict(set)
        
        for (l, v) in self.relation:
            self.relation_map[l].add(v)
            self.relation_inv_map[v].add(l)
                
        if o is not None:
            self.objects = list(o)
            for obj in o:
                self.o2A[obj] = self.relation_map[obj]
        
        if a is not None:
            self.attributes = list(a)
            for attr in a:
                self.a2O[attr] = self.relation_inv_map[attr]
                
    def f(self, o_set):
        if len(o_set) == 0:
            return set(self.attributes)
        l_o_set = list(o_set)
        a_set = self.o2A[l_o_set[0]].copy()
        for i in range(1, len(l_o_set)):
            a_set.intentsection_update(self.o2A[l_o_set[i]])
        return a_set
        
    def f_(self, oelem):
        return self.o2A[oelem]

    def g(self, a_set):
        if len(a_set) == 0:
            return set(self.objects)
        l_a_set = list(a_set)
        o_set = self.a2O[l_a_set[0]].copy()
        for i in range(1, len(l_a_set)):
            o_set &= self.a2O[l_a_set[i]]
        return o_set

    def recover_database(self):
        database = [self.o2A[i] for i in range(len(self.objects))]
        return database

    def object_concept(self, object):
        Y = self.f_(object)
        return Concept(self.g(Y), Y)

    def attribute_concept(self, attr):
        X = self.g(attr)
        return Concept(X, self.f(X))
        
class ClosedByOne(object):
    def __init__(self, context):
        self.debug_print = False
        self.L = []
        self.ctx = context
        
    def close_by_one(self):
        for gid in self.ctx.objects:
            set_g = set({gid})
            fg = self.ctx.f(set_g)
            gfg = self.ctx.g(fg)
            self.process(set_g, gid, gfg, fg)
        return self.L
    
    def process(self, A, gid, C, D):
        rset = [v for v in C if v not in A and v < gid]
        
        if len(rset) == 0:
            self.L.append(Concept(C, D, len(self.L)))
            fset = [x for x in self.ctx.objects if x > gid and x not in C]
            for f in fset:
                Z = C.copy()
                Z.add(f)
                F = self.ctx.f_(f)
                Y = D.intersection(F)
                X = self.ctx.g(Y)
                self.process(Z, f, X, Y)
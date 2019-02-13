# -*- coding: utf-8 -*-

class Concept(object):
    """Formal Concept (X, Y)"""
    def __init__(self, X, Y):
        self.intent = X
        self.extent = Y
        self.lenX = len(X)
        self.lenY = len(Y)

    """ For set check """
    def __len__(self):
        if len(self.X) == 0 and len(self.Y) == 0:
            return 0
        elif len(self.X) == 0:
            return len(self.Y);
        elif len(self.Y) == 0:
            return len(self.X)
        else:
            return len(self.X) + len(self.Y)

    def __hash__(self):
        if len(self.intent) == 0 and len(self.extent) == 0:
            return 1
        elif len(self.extent) == 0:
            return hash(list(self.intent)[0])
        elif len(self.intent) == 0:
            return hash(list(self.extent)[0])
        else:
            return hash(list(self.intent)[0]) ^ hash(list(self.extent)[0])

    def __eq__(self,other):
        return self.intent == other.intent and self.extent == other.extent

    """ String Representation """
    def set2string(self,s):
        ans = "{"
        i = 0
        N = len(s)
        for v in s:
            i += 1
            ans += "%d" % v
            if i < N:
                ans += ","
        ans += "}"
        return ans

    def __str__(self):
        return "(" + self.set2string(self.intent) + "," + self.set2string(self.extent) + ")"


class context:
    """ The formal context (O, A, I) """
    def __init__(self, relation, o=None, a=None):
        # initialize
        self.relation = relation
        self.objects = []
        self.attributes = []
        self.o2A = dict()
        self.a2O = dict()

        # Relation (set of tuples) --> Dictionary
        self.relation_map     = {}
        self.relation_inv_map = {}
        for (l, v) in self.relation:
            if l not in self.relation_map:
                self.relation_map[l] = {v}
            else:
                self.relation_map[l].add(v)
            if v not in self.relation_inv_map:
                self.relation_inv_map[v] = {l}
            else:
                self.relation_inv_map[v].add(l)

        # Objects and f
        if o is not None:
            self.objects = list(o)
            for obj in o:
                self.o2A[obj] = self.relation_map[obj]

        # Attributes and g
        if a is not None:
            self.attributes = list(a)
            for attr in a:
                self.a2O[attr] = self.relation_inv_map[attr]


    """ Galois Connection 1: f """
    def f(self, o_set):
        if len(o_set) == 0:
            return set(self.attributes)
        l_o_set = list(o_set)
        a_set = self.o2A[l_o_set[0]].copy()
        for i in range(1, len(l_o_set)):
            a_set.intersection_update(self.o2A[l_o_set[i]])
        return a_set

    def f_(self, oelem):
        return self.o2A[oelem]

    """ Galois Connection 2: g """
    def g(self, a_set):
        if len(a_set) == 0:
            return set(self.objects)
        l_a_set = list(a_set)
        o_set = self.a2O[l_a_set[0]].copy()
        for i in range(1, len(l_a_set)):
            o_set &= self.a2O[l_a_set[i]]
        return o_set


class CloseByOne(object):
    """A fundamental algorithm: Close-By-One"""
    def __init__(self, context):
        self.debug_print = False
        self.L = set()
        self.ctx = context

    """ Entry Point """
    def close_by_one(self):
        for gid in self.ctx.objects:
            set_g = set({gid})
            fg    = self.ctx.f(set_g)
            gfg   = self.ctx.g(fg)
            self.process(set_g, gid, gfg, fg)
        return self.L

    """ Bottom up genelation """
    def process(self, A, gid, C, D):
        rset = [v for v in C if v not in A and v < gid]
        if len(rset) == 0:
            if self.debug_print:
                print(" ** Add ({},{})".format(C, D))
            self.L.add(Concept(C,D))

            fset = [x for x in self.ctx.objects if x > gid and x not in C]
            for f in fset:
                Z = C.copy(); Z.add(f)
                F = self.ctx.f_(f)
                Y = D.intersection(F)
                X = self.ctx.g(Y)
                self.process(Z, f, X, Y)



# sample function for test
def sample():
    o_all = list([0,1,2,3])
    a_all = list([0,1,2])
    rel = list([(0,0), (0,1), (1,1,), (1,2), (2,1), (3,2)])
    ct = context(rel, o_all, a_all)
    alg = CloseByOne(ct)
    set_of_concepts = alg.close_by_one()

    for p in set_of_concepts:
        print(p)


if __name__ == '__main__':
    sample()

import itertools as itrt
import pandas as pd
from mpmath import gamma, log
import json
import networkx as nx

# r = nombre de valeurs différentes que peut prendre la variable x_i
# q = nombre d'instanciations possibles que les parents de x_i peuvent prendre (se référer au graphe)
    # Par exemple, pour passengerclass, q = r(fare)
        # Pour citricacid, on aura q = r(volatileacidity) * r(fixedacidity)
# m_ijk = nombre de fois dans les données où x_i = k et que les parents de x_i prennent la j_ème instanciation possible

def graph_from_json(path:str)->nx.DiGraph:
    obj = json.load(open(path))
    edges = [tuple(e) for e in obj["edges"]]
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    return graph

class Scoring:

    def __init__(self, G:nx.DiGraph, D:pd.DataFrame):
        self.G = G
        self.D = D
    
    # X_1 = age, X_2 = portembarked, ...

    # Nombre de valeurs que x_i prend
    def r(self, x_i:str)->int:
        return len(set(self.D[x_i]))


    def get_parents(self, node:str)->list:
        return list(self.G.predecessors(node))
    

    def q(self, x_i:str)->int:
        result = 1

        for i in self.get_parents(x_i):
            result *= self.r(i)
        
        return result


    def get_possible_instances(self, x_i:str)->tuple:
        return tuple(set(self.D[x_i]))


    # Par exemple, si les parents prennent les valeurs 0 ou 1, et 0 ou 1 ou 2, on aura [(0,1), (0,1,2)]
    # j est un parent spécifique (numéroté)
    def pi(self, x_i:str, j:int=None)->list|tuple:

        parents_instances = [self.get_possible_instances(parent) for parent in self.get_parents(x_i)]

        pairs = list(itrt.product(*parents_instances))

        if j:
            assert j < len(pairs)
        
        return pairs[j] if j else pairs


    def m(self, x_i:str, j:int, k: int)->int:

        parents = self.get_parents(x_i)
        column = self.D[x_i]
        result = 0
        j_e_ins = self.pi(x_i, j)

        # assert len(parents) == len(j_e_ins)
        # assert k in get_possible_instances(x_i)

        for index, i in enumerate(column):
            if i == k:
                for index_p, p in enumerate(parents):

                    parent_col_val = self.D[p][index]
                    j_eme_ins_parent = j_e_ins[index_p]

                    if parent_col_val == j_eme_ins_parent:
                        result += 1

        return result


    def score(self)->float:
        result = 0

        for i in self.G.nodes:
            
            for j in range(1, self.q(i)):

                temp_res = log(
                    gamma(self.r(i)) / gamma(self.r(i)+self.m(i, j, 0))
                ) + sum([
                    log(gamma(1+ self.m(i, j, k))) for k in range(1, self.r(i))
                ])

                result += temp_res

        return result


small = Scoring(
    G=graph_from_json('graphs/small.json'),
    D=pd.read_csv('datasets/small.csv')
)

medium = Scoring(
    G=graph_from_json('graphs/medium.json'),
    D=pd.read_csv('datasets/medium.csv')
)

print(small.score())
print(medium.score())
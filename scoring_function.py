import enum
import itertools as itrt
import pandas as pd
from mpmath import gamma, log
import json
import networkx as nx
import numpy as np
from pyrsistent import m

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

        result=0
        parents = self.get_parents(x_i)
                
        if(len(parents) != 0):
            
            instances = self.pi(x_i)
        
            for i, value in enumerate(self.D[x_i]):
        
                count = 0

                for l, value in enumerate(instances[j-1]):
                    
                    if self.D[x_i][i] == k and self.D[parents[l]][i] == instances[j-1][l]:
                        count+=1
                        
                    
                if(count==len(instances[j-1])):
                    result+=1

            return result
        
        else:

            for i, value in enumerate(self.D[x_i]):
                if self.D[x_i][i] == k:
                    result+=1
                
            return result    


    def score(self)->float:
        print(self.m("age", 1, 1))

small = Scoring(
    G=graph_from_json('graphs/small.json'),
    D=pd.read_csv('datasets/small.csv')
)

medium = Scoring(
    G=graph_from_json('graphs/medium.json'),
    D=pd.read_csv('datasets/medium.csv')
)

print(small.score())
# print(medium.score())
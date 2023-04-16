attributsPossibles = ["age","portembarked","fare","numparentschildren","passengerclass","sex","numsiblings","survived"]

from networkx.generators.random_graphs import erdos_renyi_graph
import matplotlib.pyplot as plt
import random
import networkx as nx
from scoring_function import Scoring
import pandas as pd

# Creer une liste de graphes aléatoires, list de taille nb
def createRndG(nb):
    listGraphes = []

    for i in range(nb):
        graph = nx.DiGraph()
        for at in attributsPossibles:
            graph.add_node(at)
        while nx.is_directed_acyclic_graph(graph):
            randomEdge = (random.choice(attributsPossibles), random.choice(attributsPossibles))
            # print(randomEdge)
            if randomEdge[0] != randomEdge[1]:
                graph.add_edge(randomEdge[0], randomEdge[1])
        listGraphes.append(graph)
    # nx.draw_networkx(graph, arrows=True)
    # plt.show()
    return listGraphes

data = pd.read_csv('datasets/small.csv')

def bestGraph(nb):
    res = {}
    graphes = createRndG(nb)
    for g in graphes:
        scoring = Scoring(g, data)
        res[scoring.score()] = g.edges()
    myKeys = list(res.keys())
    myKeys.sort()
    resSorted = {i: res[i] for i in myKeys}

    return [{'score': float(score) , 'graph': list(graph)} for score, graph in resSorted.items()]

# print(bestGraph(10))


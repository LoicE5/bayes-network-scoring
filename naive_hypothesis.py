import pandas as pd
import networkx as nx

df = pd.read_csv("datasets/small.csv")

graph_nodes = ["age", "portembarked", "fare", "numparentschildren", "passengerclass", "sex", "numsiblings", "survived"]

graph_edges = [(i, "survived") for i in graph_nodes if i != "survived"]

graph = nx.DiGraph()
graph.add_edges_from(graph_edges)

from test_code_valou import p

print(p(df, "survived", 1, {n:1 for n in graph_nodes if n !=  "survived"}))
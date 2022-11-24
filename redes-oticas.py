#pip install dijkstra
from dijkstra import DijkstraSPF, Graph
import data

combs = []
for x, y in data.c239_adjacency_list.items():
    for z in y:
        combs.append((x, z))

edge_weights = dict(zip(combs, data.c239_length))

graph = Graph(data.c239_adjacency_list, edge_weights)

for i in range(1, len(data.c239_adjacency_list.keys())+1):
    for j in range(1, len(data.c239_adjacency_list.keys())+1):
        print(f"Link: ({i},{j})")
        dijkstra = DijkstraSPF(graph, i)
        print(f"Path: {dijkstra.get_path(j)}")
        print(f"Distance of path ({i},{j}): {dijkstra.get_distance(j)} km")

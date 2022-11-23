#pip install dijkstra
from dijkstra import DijkstraSPF, Graph

#definição do graph
"""
adjacency_list = {1: (2, 6),
                  2: (1, 3, 6),
                  3: (2, 4, 5),
                  4: (3, 5),
                  5: (3, 4, 6),
                  6: (1, 2, 5)
                  }



edge_weights = {(1, 2): 500,
                (1, 6): 800,
                (2, 1): 500,
                (2, 3): 500,
                (2, 6): 300,
                (3, 2): 500,
                (3, 4): 500,
                (3, 5): 300,
                (4, 3): 500,
                (4, 5): 800,
                (5, 3): 300,
                (5, 4): 800,
                (5, 5): 500,
                (6, 1): 800,
                (6, 2): 300,
                (6, 5): 500
                }
graph = Graph(adjacency_list, edge_weights)
dijkstra = DijkstraSPF(graph, 1)
print(dijkstra.get_path(4))
print(dijkstra.get_distance(4))
"""

"""
dicionário:
nó atual: lista com os nos adjacentes
"""
adjacency_list = {1: (2, 6),
                  2: (1, 3, 6),
                  3: (2, 4, 5),
                  4: (3, 5),
                  5: (3, 4, 6),
                  6: (1, 2, 5)
                  }
"""
custo de cada link pela ordem do dicionário acima
"""
length = [500, 800, 500, 500, 300, 500, 500, 300, 500, 800, 300, 800, 500, 800, 300, 500]

combs = []
for x, y in adjacency_list.items():
    for z in y:
        combs.append((x, z))

edge_weights = dict(zip(combs, length))

graph = Graph(adjacency_list, edge_weights)
dijkstra = DijkstraSPF(graph, 1)
print(dijkstra.get_path(4))
print(dijkstra.get_distance(4))

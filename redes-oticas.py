# pip install dijkstra
# pip install tabulate
from dijkstra import DijkstraSPF, Graph
import data
import tabelas

# cria o dicionário para o dijkstra com base nos caminhos e nas ligações

combs = []
for x, y in data.t1_adjacency_list.items():
    for z in y:
        combs.append((x, z))

edge_weights = dict(zip(combs, data.t1_length))

graph = Graph(data.t1_adjacency_list, edge_weights)

# encontra os caminhos mais curtos para qq nos (não tem matriz de trafego)

for i in range(1, len(data.t1_adjacency_list.keys()) + 1):
    for j in range(1, len(data.t1_adjacency_list.keys()) + 1):

        print(f"Link: ({i},{j})")
        dijkstra = DijkstraSPF(graph, i)
        print(f"Path: {dijkstra.get_path(j)}")
        print(f"Distance of path ({i},{j}): {dijkstra.get_distance(j)} km")


# encontra os caminhos mais curtos para qq nos com base na matrix de tráfego

spf = []
for i, j in enumerate(data.t1_traffic_matrix):
    print(i, j)
    for s, k in enumerate(j):
        if k != 0:
            print(f"Link: ({i + 1},{s + 1})")
            dijkstra = DijkstraSPF(graph, i + 1)
            print(f"Path: {dijkstra.get_path(s + 1)}")
            print(f"Distance of path ({i + 1},{s + 1}): {dijkstra.get_distance(s + 1)} km")
            spf.append((dijkstra.get_path(s + 1), dijkstra.get_distance(s + 1)))

# shortest path first (ordena por distancia, em caso de empate pelo numero de nós -- menos nos aparecem primeiro)
spf.sort(key=lambda var: (var[1], len(var[0])))

# remove as duplicadas pk esta lib de dijsktra é unidirecional precisamos de meter os dois caminhos ex. (1,2) e (2,1)

for i in spf:
    a = (i[0][::-1], i[1])
    if a in spf:
        spf.remove(a)

print(spf)
tabelas.tabelas(spf, ["path", "km"])
tabelas.tabelas(data.t1_traffic_matrix, [i for i in range(1, 7)], [i for i in range(1, 7)])

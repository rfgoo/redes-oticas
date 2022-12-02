# pip install dijkstra
# pip install tabulate


from dijkstra import DijkstraSPF, Graph
import data
import tabelas

# cria o dicionário para o dijkstra com base nos caminhos e nas ligações

"""
combs = []
for x, y in data.t1_adjacency_list.items():
    for z in y:
        combs.append((x, z))

edge_weights = dict(zip(combs, data.t1_length))

graph = Graph(data.t1_adjacency_list, edge_weights)

"""
combs = []
for x, y in data.c239_adjacency_list.items():
    for z in y:
        combs.append((x, z))

edge_weights = dict(zip(combs, data.c239_length))

graph = Graph(data.c239_adjacency_list, edge_weights)

# encontra os caminhos mais curtos para qq nos (não tem matriz de trafego)


def get_paths(adjacency, graf, matrix=False):
    """
    :param adjacency: (dict) um dicionario com key: nó; value: lista com as suas ligações
    :param graf: (Objeto Graph) objeto graph do dijkstra
    :param matrix: (lista de listas) matrix de trafego, pode ser omitida caso nao exista
    :return spf (list): uma lista com todos os caminhos e a sua distancia,
            ordenados por ordem crscente de distancia e numero de saltos
    """

    spf = []
    if not matrix:
        for i in range(1, len(adjacency.keys()) + 1):
            for j in range(1, len(adjacency.keys()) + 1):
                dijkstra = DijkstraSPF(graf, i)
                spf.append((dijkstra.get_path(j), dijkstra.get_distance(j)))

        # encontra os caminhos mais curtos para qq nos com base na matrix de tráfego

    else:
        for i, j in enumerate(matrix):
            print(i, j)
            for s, k in enumerate(j):
                if k != 0:
                    dijkstra = DijkstraSPF(graf, i + 1)
                    spf.append((dijkstra.get_path(s + 1), dijkstra.get_distance(s + 1)))

    # shortest path first (ordena por distancia, em caso de empate pelo numero de nós -- menos nos aparecem primeiro)
    spf.sort(key=lambda var: (var[1], len(var[0])))

    # remove as duplicadas pk esta lib de dijsktra é unidirecional precisamos de meter os dois caminhos ex. (1,2) e (2,1)
    # pode dar problemas se o dijkstra nao der o mesmo caminho para 25 e 52 (deve estar resolvido)

    plh = [x for x in spf if x[1] != 0]

    for j in plh:
        s = j[0][0]
        d = j[0][-1]
        for i in plh:
            if i[0][0] == d and i[0][-1] == s:
                plh.remove(i)
    return plh


#spf_list = get_paths(data.t1_adjacency_list, graph, data.t1_traffic_matrix)
spf_list = get_paths(data.c239_adjacency_list, graph)
print(spf_list)
tabelas.tabelas(spf_list, ["path", "km"])
tabelas.tabelas(data.t1_traffic_matrix, [i for i in range(1, 7)], [i for i in range(1, 7)])

def avalia(paths,links, links_rev):
    if paths == []:
        return 0
    for li in paths:
        if li in links:
            return 1
        elif li in links_rev:
            return 1
    return 0

def fisrt_fist():
    # lista de lambdas: pos0 é o comp de onda, pos 1 é a lista de nós por onde passa, pos 2 é o contador de quantos nos passa
    wave_lens = [[0, [], 0]]
    tmp = [[0, []]]

    for i in spf_list:
        x = 0
        links_path = []
        links_path_rev = []
        for j in range(len(i[0]) - 1):
            links_path.append(i[0][j:j + 2])
            links_path_rev = [b[::-1] for b in links_path]

        for lamb in wave_lens:
            var = avalia(lamb[1], links_path, links_path_rev)
            if var == 0:
                break
            elif var!=0:
                x += 1

        if len(wave_lens) == x:
            wave_lens.append([x, [], 0])
            tmp.append([x, []])
            if len(links_path) > 1:
                for link in links_path:
                    wave_lens[x][1].append(link)
                tmp[x][1].append(i[0])
            else:
                if len(links_path) > 1:
                    for link in links_path:
                        wave_lens[x][1].append(link)
                    tmp[x][1].append(i[0])

        else:
            if len(links_path) > 1:
                for link in links_path:
                    wave_lens[x][1].append(link)
                tmp[x][1].append(i[0])
            else:

                wave_lens[x][1].append(i[0])
                tmp[x][1].append(i[0])

    return tmp


for i in fisrt_fist():
    print(i)

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
                print(f"Link: ({i},{j})")
                dijkstra = DijkstraSPF(graf, i)
                print(f"Path: {dijkstra.get_path(j)}")
                print(f"Distance of path ({i},{j}): {dijkstra.get_distance(j)} km")
                spf.append((dijkstra.get_path(j), dijkstra.get_distance(j)))

        # encontra os caminhos mais curtos para qq nos com base na matrix de tráfego

    else:
        for i, j in enumerate(matrix):
            print(i, j)
            for s, k in enumerate(j):
                if k != 0:
                    print(f"Link: ({i + 1},{s + 1})")
                    dijkstra = DijkstraSPF(graf, i + 1)
                    print(f"Path: {dijkstra.get_path(s + 1)}")
                    print(f"Distance of path ({i + 1},{s + 1}): {dijkstra.get_distance(s + 1)} km")
                    spf.append((dijkstra.get_path(s + 1), dijkstra.get_distance(s + 1)))

    # shortest path first (ordena por distancia, em caso de empate pelo numero de nós -- menos nos aparecem primeiro)
    spf.sort(key=lambda var: (var[1], len(var[0])))

    # remove as duplicadas pk esta lib de dijsktra é unidirecional precisamos de meter os dois caminhos ex. (1,2) e (2,1)
    # pode dar problemas se o dijkstra nao der o mesmo caminho para 25 e 52 (deve estar resolvido)

    for i in spf:
        s = i[0][0]
        d = i[0][-1]
        for j in spf:
            print(i)
            if j[0][0] == d and j[0][-1] == s or j[1] == 0:
                spf.remove(j)
    return spf


spf_list = get_paths(data.t1_adjacency_list, graph, data.t1_traffic_matrix)
print(spf_list)
tabelas.tabelas(spf_list, ["path", "km"])
tabelas.tabelas(data.t1_traffic_matrix, [i for i in range(1, 7)], [i for i in range(1, 7)])

# lista de lambdas: pos0 é o comp de onda, pos 1 é a lista de nós por onde passa, pos 2 é o contador de quantos nos passa
wave_lens = [[0, [], 0]]
tmp = [[0, []]]


x = 0
for i in spf_list:
    if len(i[0]) == 2 and i[0] not in wave_lens[x][1]:
        wave_lens[x][1].append(i[0])
        tmp[x][1].append(i[0])
        #print(wave_lens)
        x = 0
    else:
        links_path = []
        links_path_rev = []
        for j in range(len(i[0]) - 1):
            # print(i[0])
            # print(i[0][j:j+2])
            links_path.append(i[0][j:j + 2])
            #links_path_rev = [b[::-1] for b in links_path]
            print(links_path)
            print(links_path_rev)

        flag = True
        flag_mais1 = True
        for k in links_path:
            if flag:
                for l in range(len(wave_lens)):
                    print(k)
                    if k not in wave_lens[l][1] and flag_mais1:
                        print("here", k[0])
                        #wave_lens[x][1].append(i[0])
                        flag = True
                        pass
                    else:
                        if flag:
                            x += 1
                            flag_mais1 = False
                        if len(wave_lens) == x:
                            wave_lens.append([x,[],0])
                            tmp.append([x, []])
                            for link in links_path:
                                # print(links_path)
                                wave_lens[x][1].append(link)
                            tmp[x][1].append(i[0])
                            x = 0
                            flag = False
                            break
        if flag:
            for link in links_path:
                # print(links_path)
                wave_lens[x][1].append(link)
            tmp[x][1].append(i[0])
            x = 0




    """else:
        links_path = []
        links_path_rev = []
        for j in range(len(i[0]) - 1):
            # print(i[0])
            # print(i[0][j:j+2])
            links_path.append(i[0][j:j + 2])
            links_path_rev = [b[::-1] for b in links_path]
        print(links_path)
        print(links_path_rev)
        """
    #elif len(i[0]) > 2:
    """else:
        links_path = []
        links_path_rev = []
        for j in range(len(i[0])-1):
            #print(i[0])
            #print(i[0][j:j+2])
            links_path.append(i[0][j:j+2])
            links_path_rev = [b[::-1] for b in links_path]
        print(links_path_rev)
        print(links_path)
        while len(links_path) != 0:
            print(links_path, len(links_path))
            for var, var_rev in zip(links_path, links_path_rev):
                print("oi")
                print(var, var_rev)
                print("oi")
                for l in range(len(wave_lens)):
                    if var in wave_lens[l][1] or var_rev in wave_lens[l][1]:
                        x += 1
                        if len(wave_lens) == x:
                           # print(len(wave_lens), x)
                            wave_lens.append([x,[],0])
                            for link in links_path:
                                # print(links_path)
                                wave_lens[x][1].append(link)
                            x = 0
                            links_path = []
                            print(wave_lens)
                            print("append")
                        print("oi",x)
                        break
                    else:
                        for link in links_path:
                           # print(links_path)
                            wave_lens[x][1].append(link)

                        x = 0
                        print("CHEGUEIIIII")

                        links_path = []
                        print(wave_lens)
                        break
"""
for i in tmp:
    print(i)

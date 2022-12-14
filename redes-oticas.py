# pip install dijkstra
# pip install tabulate
import random

from dijkstra import DijkstraSPF, Graph
import data
import tabelas

# cria o dicionário para o dijkstra com base nos caminhos e nas ligações

"""
combs = []
for a, y in data.t1_adjacency_list.items():
    for z in y:
        combs.append((a, z))

edge_weights = dict(zip(combs, data.t1_length))

graph = Graph(data.t1_adjacency_list, edge_weights)
"""

combs = []
for a, y in data.c239_adjacency_list.items():
    for z in y:
        combs.append((a, z))

edge_weights = dict(zip(combs, data.c239_length))

graph = Graph(data.c239_adjacency_list, edge_weights)

# encontra os caminhos mais curtos para qq nos (não tem matriz de trafego)


def get_paths(adjacency, graf, matrix=False):
    """
    Com base no grafo e numa matrix de trafego que pode ser omitida, gera todos os caminhos possiveis entre os nós.
    Ordenado pelos caminhos mais curtos primeiro.
    Remove ainda entradas duplicadas, isto é licação 2->5 é igual a ligação 5->2. Remove a ultima.

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

    plh = [b for b in spf if b[1] != 0]

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


def avalia(paths, links, links_rev):
    """

    :param paths: caminhos com lambdas já atribuidos.
    :param links: caminho que estamos a avaliar dividido nos seus links ex. [2,3,4] origina [[2,3],[3,4]]
    :param links_rev: igual a links, mas para avaliar o reverso ex. [2,3,4] origina [[3,2],[4,3]]
    :return: 0 se o link nao estiver no caminho, nem no caminho reverso. 1 caso já se encontre.
    """
    if not paths:
        return 0
    for li in paths:
        if li in links:
            return 1
        elif li in links_rev:
            return 1
    return 0


def get_paths(i):
    """
    Função auxiliar que dado um caminho ex [2,4,5] retorna cada link desse caminho ex [[2,4],[4,5]] e o seu reverso [[4,2],[5,4]]
    :param i: Lista com o caminho, no formato: [2, 4, 5]
    :return: duas listas, uma com o caminho e outra com o caminho reverso, ex  lp = [[2,4],[4,5]], lpr = [[4,2],[5,4]]
    """
    lp = []
    lpr = []
    for j in range(len(i[0]) - 1):
        lp.append(i[0][j:j + 2])
        lpr = [b[::-1] for b in lp]
    return lp, lpr


def give_wavelengths(mode="FF"):
    """
    Função que atribui comprimentos de onda a ligações. Utiliza a lista de caminhos já ordenados pelo menor comprimento
    ao maior, e atribui a cada caminho dessa lista, sequencialmente, um comprimento de onda, tendo em conta o modo de
    trabalho em questa, dado pela variavel mode.
    :param mode: default (can be omitted) FF (first-fit),
                MU (most used) needs to be specified,
                R (random) needs to be specified.
    """
    # lista de lambdas: pos0 é o comp de onda, pos 1 é a lista de nós por onde passa, pos 2 é o contador de quantos nos passa
    wave_lens = [[0, [], 0]]
    tmp = [[0, []]]
    lisa = []
    for i in spf_list:
        x = 0
        links_path, links_path_rev = get_paths(i)

        if mode == "MU":
            wave_lens.sort(key=lambda vari: vari[2], reverse=True)
            #print(wave_lens)
        if mode != "R":
            for lamb in wave_lens:
                var = avalia(lamb[1], links_path, links_path_rev)
                if var == 0:
                    break
                elif var != 0:
                    x += 1

        elif mode == "R":
            var = 1
            tested = []
            while var == 1:
                rand = random.randint(0, len(wave_lens) - 1)
                var = avalia(wave_lens[rand][1], links_path, links_path_rev)
                if rand not in tested:
                    tested.append(rand)
                if var == 0:
                    x = rand
                    break
                if len(tested) == len(wave_lens):
                    x = len(wave_lens)
                    break

        if len(wave_lens) == x:
            wave_lens.append([x, [], 0])
            tmp.append([x, []])
            if len(links_path) > 1:
                for link in links_path:
                    wave_lens[x][1].append(link)
                wave_lens[x][2] += len(i[0])-1
                tmp[x][1].append(i[0])
                lisa.append((i[0], x))
            else:
                if len(links_path) > 1:
                    for link in links_path:
                        wave_lens[x][1].append(link)
                    wave_lens[x][2] += len(i[0])-1
                    tmp[x][1].append(i[0])
                    lisa.append((i[0], x))

        else:
            if len(links_path) > 1:
                for link in links_path:
                    wave_lens[x][1].append(link)
                wave_lens[x][2] += len(i[0])-1
                tmp[x][1].append(i[0])
                lisa.append((i[0], x))
            else:

                wave_lens[x][1].append(i[0])
                wave_lens[x][2] += len(i[0])-1
                tmp[x][1].append(i[0])
                lisa.append((i[0], x))
    print("MODO = ", mode)
    tabelas.tabelas(lisa, ["id", "path", "Lambda"])
    return


give_wavelengths(mode="FF")
give_wavelengths(mode="MU")
give_wavelengths(mode="R")

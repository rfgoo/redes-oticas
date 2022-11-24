# dicionário:
# nó atual: lista com os nos adjacentes
# Topologia da parte 1

t1_adjacency_list = {1: (2, 6),
                     2: (1, 3, 6),
                     3: (2, 4, 5),
                     4: (3, 5),
                     5: (3, 4, 6),
                     6: (1, 2, 5)
                     }

# custo de cada link pela ordem do dicionário acima
# Topologia da parte 1

t1_length = [500, 800, 500, 500, 300, 500, 500, 300, 500, 800, 300, 800, 500, 800, 300, 500]

# distancias da topologia cost 239:
c239_length = [953, 622, 361, 641,
               953, 356, 321, 343,
               622, 356, 576, 171, 318,
               361, 576, 281, 877, 525,
               321, 171, 190, 266, 697,
               318, 190, 594, 294, 251,
               641, 281, 594, 529, 594,
               343, 877, 266, 294, 490, 641,
               251, 529, 490, 594, 261,
               525, 251, 594, 625,
               697, 641, 261, 625,
               ]

# Topologia da rede COST 239:
c239_adjacency_list = {1: (2, 3, 4, 7),
                       2: (1, 3, 5, 8),
                       3: (1, 2, 4, 5, 6),
                       4: (1, 3, 7, 8, 10),
                       5: (2, 3, 6, 8, 11),
                       6: (3, 5, 7, 8, 9),
                       7: (1, 4, 6, 9, 10),
                       8: (2, 4, 5, 6, 9, 11),
                       9: (6, 7, 8, 10, 11),
                       10: (4, 7, 9, 11),
                       11: (5, 8, 9, 10),
                       }

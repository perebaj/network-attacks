#!/usr/bin/python3
# -*- coding: utf-8 -


import igraph as ig
import numpy as np
from Manipulate import ManipulateGraph
import networkx as nx
from Attack_Functions import attack_degree_igraph, random_attack_igraph, attack_transitivity_igraph, attack_betweenness_igraph

NODES_NUMBER        = 10000
ITERATION_REMOVALS  = 10


manipulate  = ManipulateGraph()
barabasi_nx = nx.barabasi_albert_graph(NODES_NUMBER, 2, seed=192)
barabasi_ig = manipulate.convert_networkx_to_igraph(barabasi_nx)
print(manipulate.degree_average_nx(barabasi_nx))
print(manipulate.degree_average_ig(barabasi_ig))

largest_cc, transitivity    = random_attack_igraph(barabasi_ig, ITERATION_REMOVALS)
largest_cc1, transitivity1  = attack_degree_igraph(barabasi_ig, ITERATION_REMOVALS)
# largest_cc2, transitivity2  = attack_transitivity_igraph(barabasi_ig, ITERATION_REMOVALS)

np.savetxt('largest_cc_barabasi_randomATT', largest_cc)
np.savetxt('transitivity_barabasi_randomATT', transitivity)
np.savetxt('largest_cc_barabasi_degreeATT', largest_cc1)
np.savetxt('transitivity_barabasi_degreeATT', transitivity1)
# np.savetxt('largest_cc_barabasi_transitivityATT', largest_cc2)
# np.savetxt('transitivity_barabasi_transitivityATT', transitivity2)

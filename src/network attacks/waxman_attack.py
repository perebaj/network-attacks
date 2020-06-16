#!/usr/bin/python3
# -*- coding: utf-8 -

import pickle
import igraph as ig
import numpy as np
import networkx as nx
from Manipulate import ManipulateGraph
from Attack_Functions import attack_degree_igraph, random_attack_igraph, attack_transitivity_igraph, attack_betweenness_igraph

NODES_NUMBER        = 10000
ITERATION_REMOVALS  = 10

manipulate  = ManipulateGraph()
waxman_nx   = nx.waxman_graph(10000, alpha=0.0057, beta=1, seed=192)
waxman_ig   = manipulate.convert_networkx_to_igraph(waxman_nx)

print(manipulate.degree_average_ig(waxman_ig))
print(manipulate.degree_average_nx(waxman_nx))



largest_cc, transitivity    = random_attack_igraph(waxman_ig, ITERATION_REMOVALS)
largest_cc1, transitivity1  = attack_degree_igraph(waxman_ig, ITERATION_REMOVALS)
# largest_cc2, transitivity2  = attack_transitivity_igraph(waxman_ig, ITERATION_REMOVALS)
# 
np.savetxt('largest_cc_waxman_randomATT', largest_cc)
np.savetxt('transitivity_waxman_randomATT', transitivity)
np.savetxt('largest_cc_waxman_degreeATT', largest_cc1)
np.savetxt('transitivity_waxman_degreeATT', transitivity1)
# np.savetxt('largest_cc_waxman_transitivityATT', largest_cc2)
# np.savetxt('transitivity_waxman_transitivityATT', transitivity2)
# 
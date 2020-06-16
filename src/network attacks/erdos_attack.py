#!/usr/bin/python3
# -*- coding: utf-8 -


import igraph as ig
import numpy as np
from Manipulate import ManipulateGraph
from Attack_Functions import attack_degree_igraph, random_attack_igraph, attack_transitivity_igraph, attack_betweenness_igraph

NODES_NUMBER = 10000
ITERATION_REMOVALS = 10

manipulate  = ManipulateGraph()
erdos_ig    = ig.Graph.Erdos_Renyi(NODES_NUMBER, 4/NODES_NUMBER) 
print(manipulate.degree_average_ig(erdos_ig))

largest_cc, transitivity = random_attack_igraph(erdos_ig, ITERATION_REMOVALS)
largest_cc1, transitivity1 = attack_degree_igraph(erdos_ig, ITERATION_REMOVALS)
# largest_cc2, transitivity2 = attack_transitivity_igraph(erdos_ig, ITERATION_REMOVALS)

np.savetxt('largest_cc_erdos_randomATT', largest_cc)
np.savetxt('transitivity_erdos_randomATT', transitivity)
np.savetxt('largest_cc_erdos_degreeATT', largest_cc1)
np.savetxt('transitivity_erdos_degreeATT', transitivity1)
# np.savetxt('largest_cc_erdos_transitivityATT', largest_cc2)
# np.savetxt('transitivity_erdos_transitivityATT', transitivity2)

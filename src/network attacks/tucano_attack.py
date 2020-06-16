#!/usr/bin/python3
# -*- coding: utf-8 -

import pickle
import igraph as ig
import numpy as np
from Manipulate import ManipulateGraph
from Attack_Functions import attack_degree_igraph, random_attack_igraph, attack_transitivity_igraph, attack_betweenness_igraph

ITERATION_REMOVALS = 10

manipulate  = ManipulateGraph()
tucano00_network_ig = pickle.load(open('/home/jonathan/Documentos/network-attacks/src/Tucano Network/Bico_tucano_00_scaled_binary_network.dat', 'rb'), encoding='latin1')
tucano00_network_ig.simplify()
manipulate.degree_average_ig(tucano00_network_ig)


largest_cc, transitivity = random_attack_igraph(tucano00_network_ig, ITERATION_REMOVALS)
largest_cc1, transitivity1 = attack_degree_igraph(tucano00_network_ig, ITERATION_REMOVALS)
# largest_cc2, transitivity2 = attack_transitivity_igraph(tucano00_network_ig, ITERATION_REMOVALS)
# 
np.savetxt('largest_cc_tucano_randomATT', largest_cc)
np.savetxt('transitivity_tucano_randomATT', transitivity)
np.savetxt('largest_cc_tucano_degreeATT', largest_cc1)
np.savetxt('transitivity_tucano_degreeATT', transitivity1)
# np.savetxt('largest_cc_tucano_transitivityATT', largest_cc2)
# np.savetxt('transitivity_tucano_transitivityATT', transitivity2)

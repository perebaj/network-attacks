#!/usr/bin/python3
# coding: utf-8

import networkx
import igraph

graph_nx = networkx.waxman_graph(20)
manipulate_graphs = ManipulateGraph()
graph_ig = manipulate_graphs.convert_networkx_to_igraph2(graph_nx)
manipulate_graphs.print_nx_graph(graph_nx)
graph_ig.get_edgelist()
graph_ig.delete_edges([4])
graph_ig = graph_ig.delete_edges(4)
graph_ig = graph_ig.delete_edges([4])
graph_ig = graph_ig.delete_edges([(4,6)])

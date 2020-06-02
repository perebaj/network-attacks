#!/usr/bin/python3
# -*- coding: utf-8 -
import networkx as nx
import igraph
import numpy as np
import matplotlib.pyplot as plt
import igraph as ig
import pprint
from tqdm import tqdm


class ManipulateGraph:

    def __init__(self):
        pass

    def convert_networkx_to_igraph(self, graph_nx):
        # convert via adjacency matrix
        g2 = ig.Graph().Adjacency((nx.to_numpy_array(graph_nx) > 0).tolist())
        g2 = g2.as_undirected()
        return g2

    def edgelist_nx(self, graph_nx):
        edgelist2 = []
        for line in graph_nx.edges():
            edgelist2.append((line))
        print(line)

    def convert_igraph_to_nx(self, graph_ig):
        graph_nx = nx.Graph()  # intancia do grafo tipo networkx
        # instancia do grafo com o mesmo número de nós de {graph_ig}
        graph_nx.add_nodes_from(np.arange(graph_ig.vcount()))
        # lista de arestas do grafo {graph_ig}
        edgelist = graph_ig.get_edgelist()
        graph_nx.add_edges_from(edgelist)  # adiciona as areasta em {graph_nx}
        return graph_nx

    def convert_networkx_to_igraph2(self, graph_nx):
        return(igraph.Graph(len(graph_nx), list(zip(*list(zip(*nx.to_edgelist(graph_nx)))[:2]))))

    def print_nx_graph(self, graph_nx):
        for line in nx.generate_adjlist(graph_nx):
            print(line)

    def draw_nx(self, graph_nx):
        nx.draw(graph_nx, with_labels=True, font_weight='bold')
        plt.show()

    def confimation(self, graph_ig, graph_nx):
        igraph.summary(graph_ig)
        print(graph_nx.number_of_edges())
        print(graph_nx.number_of_nodes())

    def degree_average_nx(self, graph_nx):
        degrees = nx.degree(graph_nx)
        d = []
        for deg in degrees:
            d.append(deg[1])
        d = np.array(d)
        return np.mean(d)



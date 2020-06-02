#!/usr/bin/python3
# -*- coding: utf-8 -*-
import igraph
import numpy as np
import matplotlib.pyplot as pyplot
import math
import sys

class  SpatialNetworl():
    """
    Spatial Network Generator
    """
    RANDOM = np.random


    def generate_Waxman(self, size_of_network, parameter_list):
        """
            Parameters:
            size_of_network: Um inteiro que indica o número de nós da rede 
            parameter_list: [alpha, beta, force_connected].
                alpha: Um duble entre 0 e 1 representando a densidade de arestas curtas em relação às arestas longas.
                beta: A double representing the edge density. Um double representando a densidade das arestas
                force_connected: Um booleano indicando se o gráfico deve ser conectado(default=False).
        
            Returns:
              An igraph graph based on the Waxman mode
        """
        alpha = parameter_list[0]
        beta = parameter_list[1]
        force_connected = parameter_list[2] if len(parameter_list) > 2 else False

        # Create an undirected graph with size_of_network nodes.
        g = igraph.Graph(size_of_network)

        # Create random points in a 1x1 square.
        x = self.RANDOM.uniform(size=size_of_network)
        y = self.RANDOM.uniform(size=size_of_network)
        # print(x, y)
       
        # Create the edges.
        sq2 = math.sqrt(2)
        edges = []
        for i in range(size_of_network-1):
            has_neighbor = False
            for j in range(i+1, size_of_network):
                d = ((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** 0.5 #Distância euclidiana entre i e j correntes
                # print(d)
                p = beta * math.exp(-d / (sq2 * alpha))
                if p > 1:
                    raise Exception('P is larger than 1.')
                # print(self.RANDOM.uniform())
                if self.RANDOM.uniform() < p:
                    has_neighbor = True
                    edges.append((i, j))
            if force_connected and not has_neighbor:
                # Forcefully connects to one of the nodes.
                ps = []
                for j in range(i+1, size_of_network):
                    d = ((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** 0.5
                    p = beta * math.exp(-d / (sq2 * alpha))
                    ps.append(p)
                tot = sum(ps)
                ps = [_p*1.0/tot for _p in ps]
                j = self.RANDOM.choice(range(i+1, size_of_network), p=ps)
                edges.append((i, j))

        g.add_edges(edges)
        return g

spatialnet = SpatialNetworl()

graph = spatialnet.generate_Waxman(100, [0.4, 0.1])

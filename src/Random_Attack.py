#!/usr/bin/python3
# -*- coding: utf-8 -
import random
import numpy as np
import networkx.algorithms.cluster as nx_cluster
import networkx
from networkx.algorithms import components
from tqdm import tqdm
from Manipulate import ManipulateGraph
import igraph
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


def random_numbers(removals_number, iteration_removals):
    """
    param       {removals_number}      número de nós da rede
    param       {iteration_removals}          número remoções que serão feitas na rede
    Return:     Retorna uma lista de removals_number - iteration_removals de números aleatórios, com dimensão (i = iteration_removals & j = (removals_number - iteration_removals)/iteration_removals)
    """
    lenght_list = removals_number - iteration_removals
    random_array = np.array(random.sample(range(removals_number), lenght_list))
    return random_array.reshape(iteration_removals, lenght_list/iteration_removals).T


def random_attack(graph, nodes_number, iteration_removals):
    # lista onde estão os valores de clusterização da rede depois da remoção dos nos
    after_removals = []
    # number_nodes_largest_cc = [] #número de nós do maior componente da rede
    lenght_range = int((nodes_number - iteration_removals)/iteration_removals)
    for _ in tqdm(range(lenght_range)):
        # retorna um set, com os nos que representam o maior componente conexo da rede
        largest_cc = max(networkx.connected_components(graph), key=len)
        # se o tamanho do maior componente conexo por menor que o número de nos que quero remover, sair do loop
        if len(largest_cc) < iteration_removals:
            break
        # number_nodes_largest_cc.append(len(largest_cc))
        # remove iterations_removals do maior componente conexo da rede
        graph.remove_nodes_from(random.sample(largest_cc, iteration_removals))
        after_removals.append(
            np.mean(list(nx_cluster.clustering(graph).values())))
    return after_removals


def random_attack2(graph, nodes_number, iteration_removals):
    # lista onde estão os valores de clusterização da rede depois da remoção dos nos
    after_removals = []
    lenght_range = int((nodes_number - iteration_removals)/iteration_removals)
    # retorna um set, com os nos que representam o maior componente conexo da rede
    # print('largest cc: {}'.format(largest_cc))
    for _ in tqdm(range(lenght_range)):
        # se o tamanho do maior componente conexo por menor que o número de nos que quero remover, sair do loop
        largest_cc = max(networkx.connected_components(graph), key=len)
        print(len(largest_cc))
        if len(largest_cc) < iteration_removals:
            break
        removals_set = set(random.sample(largest_cc, iteration_removals))
        # print('remocoes: {}'.format(removals_set))
        largest_cc = largest_cc - removals_set
        # remove iterations_removals do maior componente conexo da rede
        graph.remove_nodes_from(removals_set)
        after_removals.append(nx_cluster.transitivity(graph))
        # after_removals.append(np.mean(list(nx_cluster.transitivity(graph).values())))
    return after_removals


def first_tuple_element(tupla):
    first_tuple_element = []
    for a_tuple in tupla:
        first_tuple_element.append(a_tuple[0])
    return first_tuple_element


def attack_degree(graph, nodes_number, iteration_removals):
    after_removals = []
    lenght_range = int((nodes_number - iteration_removals)/iteration_removals)
    degress = list(graph.degree())
    degress.sort(key=lambda x: x[1], reverse=True)
    first_element = first_tuple_element(degress)
    degress_reshaped = np.reshape(
        first_element, (iteration_removals, int(nodes_number/iteration_removals))).T

    for iterator in tqdm(range(lenght_range)):
        # remove iterations_removals do maior componente conexo da rede
        graph.remove_nodes_from(degress_reshaped[iterator])
        after_removals.append(
            np.mean(list(nx_cluster.clustering(graph).values())))
    return after_removals


def attack_degree_igraph(graph, iteration_removals):
    '''
    Ataque direcinado a uma rede, baseada no seu maior componente conexo e nós com maior grau. 
    medição da transitividade da rede para cada remoção feita

    Parametros
    ----------------------------
        graph: Grafo que será atacado
        iteration_removals: Número de nós removidos por iteração
    '''
    graph   = graph.copy()
    largest_cc   = []
    transitivity  = []
    while True:
        components      = graph.components()
        graph           = components.giant() #Maior componente conexo da rede
        size_largest_cc = graph.vcount()
        if size_largest_cc <= iteration_removals:
            break
        largest_cc.append(size_largest_cc)
        transitivity.append(graph.transitivity_undirected()) #Transitivade da rede com maior componente conexo
        degrees     = np.array(graph.degree()) #Grau de cada vértice
        probs       = degrees/degrees.sum() #Probilidades proporcionais ao grau de cada vértice
        nodes_index = np.random.choice(graph.vcount(), size=iteration_removals, replace=False, p=probs) #escolha de {iteration_removals} nós de acordo com as probabilidade para serem removidos
        graph.delete_vertices(nodes_index)
    return largest_cc, transitivity


def random_attack_igraph(graph, iteration_removals):
    '''
    Ataque aleatorio a uma rede, baseada no seu maior componente conexo e medição da transitividade da rede para cada remoção de nós

    Parametros
    ----------------------------
        graph: Grafo que será atacada
        iteration_removals: Número de nós removidos por iteração
    '''
    graph        = graph.copy()
    transitivity = []
    largest_cc   = []

    while True:
        components          = graph.components()
        graph = components.giant()
        size_largest_cc     = graph.vcount()
        if size_largest_cc <= iteration_removals:
            break
        largest_cc.append(size_largest_cc)
        transitivity.append(graph.transitivity_undirected()) #Transitivade da rede com maior componente conexo
        nodes_index         = np.random.choice(graph.vcount(), size=iteration_removals, replace=False) #escolha de {iteration_removals} nós aleatórios para serem removidos
        graph.delete_vertices(nodes_index)
    return largest_cc, transitivity


NODES_NUMBER = 10000
ITERATION_REMOVALS = 10
manipulate = ManipulateGraph()
waxman_networkx = networkx.waxman_graph(NODES_NUMBER, alpha=0.0004, beta=1, L=0.5)
waxman_igraph = manipulate.convert_networkx_to_igraph(waxman_networkx)
erdos = igraph.Graph.Erdos_Renyi(NODES_NUMBER, 4/NODES_NUMBER)
largest_cc, transitivity = random_attack_igraph(erdos, ITERATION_REMOVALS)

np.savetxt('largest_cc_erdos_randomATT', largest_cc)
np.savetxt('transitivity_cc_erdos_randomATT', transitivity)

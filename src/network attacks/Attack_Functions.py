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

def nan_replace(lista):
    for x in range(len(lista)):
        if np.isnan(lista[x]):
            lista[x] = 0
    return lista

def attack_transitivity_igraph(graph, iteration_removals):
    graph        = graph.copy()
    largest_cc   = []
    transitivity = []
    while True:
        components      = graph.components()
        graph           = components.giant() #Maior componente conexo da rede
        size_largest_cc = graph.vcount()
        largest_cc.append(size_largest_cc)
        cluster     = np.array(graph.transitivity_local_undirected(mode='zero'))
        transitivity.append(graph.transitivity_undirected()) #Transitivade da rede com maior componente conexo
        if filtro(cluster, 0) < iteration_removals:
            cluster += 1e-10
        probs       = cluster/cluster.sum() #Probilidades proporcionais ao grau de cada vértice
        # print(probs)
        nodes_index = np.random.choice(graph.vcount(), size=iteration_removals, replace=False, p=probs) #escolha de {iteration_removals} nós de acordo com as probabilidade para serem removidos
        # print(nodes_index)
        graph.delete_vertices(nodes_index)

    return largest_cc, transitivity


def attack_betweenness_igraph(graph, iteration_removals):
    graph        = graph.copy()
    largest_cc   = []
    transitivity = []
    while True:
        components      = graph.components()
        graph           = components.giant() #Maior componente conexo da rede
        size_largest_cc = graph.vcount()
        largest_cc.append(size_largest_cc)
        transitivity.append(graph.transitivity_undirected()) #Transitivade da rede com maior componente conexo
        betweenness = np.array(graph.betweenness())
        if filtro(betweenness, 0) < iteration_removals:
            break
        probs       = betweenness/betweenness.sum() 
        nodes_index = np.random.choice(graph.vcount(), size=iteration_removals, replace=False, p=probs) 
        graph.delete_vertices(nodes_index)

    return largest_cc, transitivity

def filtro(lista, filtro):
    filtrados = [x for x in lista if x > filtro]
    return len(filtrados)


# NODES_NUMBER = 1000
# ITERATION_REMOVALS = 10
# manipulate = ManipulateGraph()
# waxman = networkx.waxman_graph(10000, alpha=0.007, beta=1)
# barabasi = networkx.barabasi_albert_graph(NODES_NUMBER, 3)
# igraph = manipulate.convert_networkx_to_igraph(barabasi)
# igraphDegree = igraphRandom.copy()
# erdos = igraph.Graph.Erdos_Renyi(NODES_NUMBER, 6/NODES_NUMBER) 
# graumedio = manipulate.degree_average_nx(barabasi)
# print(graumedio)
# largest_cc2, transitivity2 = attack_degree_igraph(igraphDegree, ITERATION_REMOVALS)
# largest_cc1, transitivity1 = random_attack_igraph(igraphRandom, ITERATION_REMOVALS)
# largest_cc, transitivity = attack_betweenness_igraph(erdos, ITERATION_REMOVALS)

# print(largest_cc)

# np.savetxt('teste', largest_cc)
# np.savetxt('teste2', transitivity)
# np.savetxt('largest_cc_waxman_randomATT', largest_cc1)
# np.savetxt('transitivity_waxman_randomATT', transitivity1)



# coding: utf-8
import networkx
import igraph
graph_nx = networkx.waxman_graph(20)
graph_ig = igraph.Graph(len(graph_nx), list(zip(*list(zip(*networkx.to_edgelist(graph_nx)))[:2])))
import numpy as np
import networkx.algorithms.cluster as nx_cluster
cluster_nx = np.mean(list(nx_cluster.clustering(graph_nx).values()))
cluster_nx
nx_cluster.clustering(graph_nx).values()
graph_nx = networkx.waxman_graph(100)  
nx_cluster.clustering(graph_nx).values()
cluster_nx = np.mean(list(nx_cluster.clustering(graph_nx).values()))
cluster_nx
graph_ig = igraph.Graph(len(graph_nx), list(zip(*list(zip(*networkx.to_edgelist(graph_nx)))[:2])))
graph_ig.transitivity_avglocal_undirected()
graph_ig.transitivity_undirected()
graph_ig.transitivity_local_undirected()
cluster_ig = np.mean(graph_ig.transitivity_local_undirected())
cluster_ig
np.mean(graph_ig.transitivity_local_undirected())
graph_ig.transitivity_local_undirected()
cluster_ig = graph_ig.transitivity_local_undirected()
cluster_ig
np.nan_to_num(cluster_ig)
cluster_ig
cluster_ig = np.nan_to_num(cluster_ig)
cluster_ig
np.mean(cluster_ig)
nx_cluster.transitivity(graph_nx)
graph_ig.transitivity_avglocal_undirected()
graph_ig.transitivity_undirected()


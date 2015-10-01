import matplotlib.pyplot as plt
import networkx as nx  
import matplotlib.cm as cm
import numpy as np
from networkx.readwrite import json_graph
import json


color_edge = ['b','r','g','c','m']
color_node = ['orange','b','k']
color_source = 'r'
color_sink = 'g'

""" visualize a directed graph with highlighted edges and nodes
"""
def drawLargeGraph(G,pos,edgelists=[],nodelists=[],sources=[],sinks=[],nodesize=60):

    nx.draw_networkx_edges(G,pos,width=0.4,alpha=0.3)
    for i,nodes in enumerate(nodelists):
        nx.draw_networkx_nodes(G,pos,nodelist=nodes,
                               node_size=nodesize,
                               alpha=0.4,
                               linewidths=0.01,
                               node_color=color_node[i % len(color_node)])

    for i,edgeli in enumerate(edgelists) : 
        nx.draw_networkx_edges(G, pos, edgelist = edgeli,
                               width=1.5,
                               alpha=0.8,
                               edge_color=color_edge[i % len(color_edge)])
    nx.draw_networkx_nodes(G,pos,nodelist=sources,node_size=nodesize*1.5,
                           node_color=color_source)
    nx.draw_networkx_nodes(G,pos,nodelist=sinks, node_size=nodesize*1.5,
                           node_color=color_sink)

    plt.axis('off')
    #plt.axes().set_aspect('equal', 'datalim')
    #plt.savefig("largeGraph.png");

""" compute total length of a path as sum of edge weights
wt_attr: edge weight attribute name
"""    
def pathLen(g,path,wt_attr="weight"):
    if (len(path) <= 1):
        return 0;
    return sum( [g.edge[path[i]][path[i+1]][wt_attr] for i in range(0,len(path)-1)])

""" convert a path (sequence of nodes) into a list of edges
"""
def toEdgeList(path):
    edge_list  = []
    for i in range(0,len(path)-1):
        edge_list.append((path[i],path[i+1]))
    return edge_list

""" extract shortest path tree as a list of edges
"""
def shortestPathTree( vData):
    return [(data['parent'],v) for (v,data) in vData.iteritems() \
            if data['parent']!=None]

"""write graph to json format
"""
def writeWebFormat(g,  paths=[]):
    d = json_graph.node_link_data(g) # node-link format to serialize
    d['paths']=paths
    json.dump(d, open('graph.json','w'))
    print('Wrote node-link JSON data to graph.json')

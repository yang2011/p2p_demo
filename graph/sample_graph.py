import networkx as nx
import numpy as np
import math
import pprint
import utm



"""load california road network
node features:  x, y (utm converted coordinates)
edge features: weight (euclidean distance between 2 nodes) 
"""
def loadCalGraph():
    edgeName = "data/cal.cedge.txt"
    nodeName = "data/cal.cnode.txt"
    g = nx.DiGraph()
    file = open(nodeName)
    pos = {}
    for line in file:
        words = line.split();
        [nid,lon,lat] = [int(words[0]),float(words[1])*1e-5,float(words[2])*1e-5];
        u = utm.from_latlon(lat, lon,11)
        g.add_node(nid, x=u[0],y=u[1] ,name=id);
        pos[nid] = np.array(u[0:2]);
     
    file = open(edgeName)
    print ".. finished reading nodes";

    for line  in file:
        words = line.split();
        [eid,src,dst]=[int(words[0]),int(words[1]),int(words[2]) ]
        dist_l2 = np.linalg.norm(pos[dst]-pos[src],2)
        if (not (src == dst)):
            g.add_edge(src,dst,weight=dist_l2)
            g.add_edge(dst,src,weight=dist_l2)

    print ".. finished reading edges"
    return (g,pos)

"""make a directed graph on a 4x3 grid, all edge has unit weight
node features: x, y
""" 
def makeToyDiGraph():
    edgelist = [ (1,0),(2,1),(3,2), (4,5),(5,6),(6,7),(0,4),(5,1),(2,6),(7,3),
                 (4,8),(8,9),(9,10),(10,11),(9,5),(6,10),(11,7)]
    pos = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)]
    g = nx.DiGraph()
    for n in range(0,len(pos)):
        g.add_node(n,x=pos[n][0], y=pos[n][1] )
    g.add_edges_from(edgelist,weight=1)

    return (g, dict(enumerate(pos)))

"""make a random direct graph
"""
def makeRandomDiGraph():
    g = nx.navigable_small_world_graph(8,1,1,11,2, 42)
    g = nx.convert_node_labels_to_integers(g, 0)

    pos = nx.spectral_layout(g)
    for n,nbrs in g.adjacency_iter():
        g.node[n]['x'] = pos[n][0]
        g.node[n]['y'] = pos[n][1]
        #g.node[n]['name'] = n #str(n)
        for nbr,eattr in nbrs.items():
            eattr['weight'] = np.linalg.norm(pos[nbr]-pos[n],2) 
    
    return (g,pos)


from heapq import *
import networkx as nx 


""" status symbols in the labeling algorithm
"""
def enum(**enums):
    return type('Enum', (), enums)

Status = enum(unreached=1, labeled=2, scanned=3)


"""
relax edge (v,w) . return true if vertex label is updated
wt_attr: edge weight attribute name
"""
def relax(g,v,w,wt_attr,dv,vData):
    newDist = dv+g[v][w][wt_attr]

    if (vData[w]['ds'] > newDist ):
        vData[w]['ds'] = newDist
        vData[w]['parent'] = v
        if (vData[w]['status']== Status.unreached):
            vData[w]['status'] = Status.labeled
        return True
    return False
    
"""
labeling algorithm (Dijkstra) for finding shortest s-t path
wt_attr: edge weight attribute name
"""
def labeling(g,s,t,wt_attr='weight'):

    vData = {n:{"ds":float('inf'),
                "parent":None,
                "status":Status.unreached} for n in g}
    vData[s]['ds'] =0
    vData[s]['status'] = Status.labeled
    pqueue = [] # priority queue for sorting LABELED vertices
    heappush(pqueue, ( vData[s]['ds'] ,s))
    while (len(pqueue)>0):
        (distToSrc,v) = heappop(pqueue)
        if (v==t):
            break
        dv = vData[v]['ds']
        for w in g.neighbors(v):
                if (relax(g,v,w,wt_attr,dv,vData)):
                        heappush(pqueue,(vData[w]['ds'],w))
        vData[v]['status'] = Status.scanned
    path = []
    u = t
    while (vData[u]['parent'] != None):
            path.insert(0,u)
            u = vData[u]['parent']
    path.insert(0,s)
    return (path,vData)
    
    


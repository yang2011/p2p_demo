import numpy as np
from heapq import *
import sys
from dijkstra import *

""" compute potential function pi(v) for all node v in graph g
with destination t.
pi(v) = ||v - t||
"""
def potential_l2(g,t):
    
    pi = np.zeros( g.number_of_nodes())
    for n,d in g.nodes_iter(data=True):
        pos = np.array((d['x'],d['y']))
        target = np.array( (g.node[t]['x'], g.node[t]['y']))
        pi[n] = np.linalg.norm(pos-target)
    return pi

""" compute shortest s-t path using lower bounding algorithm (A*)
pi: potential function
wt_attr: edge weight attribute name
"""
def lowerBounding(g,s,t,pi,wt_attr):

    vData = {n:{"ds":float('inf'),
                "parent":None,
                "status":Status.unreached} for n in g}
    vData[s]['ds'] =0
    vData[s]['status'] = Status.labeled
    pqueue = [] # priority queue for sorting LABELED vertices
    heappush(pqueue, ( vData[s]['ds'] + pi[s] ,s))
    while (len(pqueue)>0):
        (kv,v) = heappop(pqueue)
        if (v==t):
            break
        dv = vData[v]['ds']
        for w in g.neighbors(v):
                if (relax(g,v,w,wt_attr,dv,vData)):
                        heappush(pqueue,(vData[w]['ds']+pi[w],w))
        vData[v]['status'] = Status.scanned
    path = []
    u = t
    while (vData[u]['parent'] != None):
            path.insert(0,u)
            u = vData[u]['parent']
    path.insert(0,s)
    return (path,vData)
    
""" symmetric lower bounding algorithm (bidirectional A*)
"""
def symmetricLowerBounding(g,s,t,pi_forward,pi_backward, wt_attr):
    gRev = g.reverse()
    vDataS = {n:{"ds":float('inf'),
                "parent":None,
                "status":Status.unreached} for n in g}
    vDataS[s]['ds'] =0
    vDataS[s]['status'] = Status.labeled
    vDataT = {n:{"ds":float('inf'),
                "parent":None,
                "status":Status.unreached} for n in g}
    vDataT[t]['ds'] =0
    vDataT[t]['status'] = Status.labeled
    pqueues = []
    pqueuet = []
    heappush(pqueues, (vDataS[s]['ds']+pi_forward[s], s))
    heappush(pqueuet, (vDataT[t]['ds']+pi_backward[t],t))
    mu = float('inf')
    
    while (len(pqueues)>0 and len(pqueuet)>0):
        # forward search
        (kv,v) = heappop(pqueues)

        if ( kv >= mu ): # stop condition
            break
        dv = vDataS[v]['ds']
        for w in g.neighbors(v):

            # prune v,w if it has been scanned by backward search
            if ( vDataT[w]['status'] == Status.scanned):
                continue

            if (relax(g,v,w,wt_attr,dv,vDataS)):
                heappush(pqueues, (vDataS[w]['ds']+pi_forward[w],w))
                
            if (vDataS[w]['ds'] +vDataT[w]['ds'] < mu):
                mu = vDataS[w]['ds'] + vDataT[w]['ds']
        vDataS[v]['status'] =Status.scanned
        
        # backward search
        (kv,v) = heappop(pqueuet)
        if (kv >= mu ): # stop condition
            break
        dv = vDataT[v]['ds']
        for w in gRev.neighbors(v):
            if (vDataS[w]['status'] == Status.scanned):
                continue

            if (relax(gRev,v,w,wt_attr,dv,vDataT)):
                heappush(pqueuet, (vDataT[w]['ds']+pi_backward[w],w))

            if (vDataS[w]['ds'] +vDataT[w]['ds'] < mu):
                mu = vDataS[w]['ds'] + vDataT[w]['ds']                
        vDataT[v]['status'] =Status.scanned
    
    path = reconstructMinPath(s,t,vDataS,vDataT)
    return (path,vDataS,vDataT)


""" reconstruct shortest s-t path from forward shortest path tree
and backward shortest path tree, given midpoint 
""" 
def reconstructMinPath(s,t,vDataS,vDataT):
    midpoints = [(vDataS[v]['ds']+ vDataT[v]['ds'],v)  for v in vDataS.keys() if \
                 (vDataS[v]['status'] != Status.unreached and \
                  vDataT[v]['status'] != Status.unreached)]

    (minPathLen,midpoint) = min(midpoints)
    print "shortest path distance: " , minPathLen, " with midpoint " , midpoint
    
    path = []
    u = midpoint
    while (vDataS[u]['parent']!=None):
        path.insert(0,u)
        u = vDataS[u]['parent']
    path.insert(0,s)
    
    u = vDataT[midpoint]['parent']
    while (vDataT[u]['parent']!=None):
        path.append(u)
        u = vDataT[u]['parent']
    path.append(t)
    return path

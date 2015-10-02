
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
    
    
"""
plain bidirectional Dijkstra
wt_attr: edge weight attribute name
"""
def bidirectionalSearch(g,s,t,wt_attr):
    gRev= g.reverse()
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
    heappush(pqueues, (vDataS[s]['ds'], s))
    heappush(pqueuet, (vDataT[t]['ds'], t))
    ds_top = 0
    dt_top = 0
    mu = float('inf') # best shortest path length found so far
    while (len(pqueues)>0 and len(pqueuet)>0):
        # forward search
        (ds_top,v) = heappop(pqueues)

        if ( ds_top + dt_top >= mu ): # stop condition
            break
        dv = vDataS[v]['ds']
        for w in g.neighbors(v):
            if (relax(g,v,w,wt_attr,dv,vDataS)):
                heappush(pqueues, (vDataS[w]['ds'],w))
                
            if ( vDataT[w]['status'] == Status.scanned and
                 vDataS[w]['ds'] +vDataT[w]['ds'] < mu):
                mu = vDataS[w]['ds'] + vDataT[w]['ds']
        vDataS[v]['status'] =Status.scanned
        
        # backward search
        (dt_top,v) = heappop(pqueuet)
        if (ds_top + dt_top >= mu): # stop condition
            break
        dv = vDataT[v]['ds']
        for w in gRev.neighbors(v):
            if (relax(gRev,v,w,wt_attr,dv,vDataT)):
                heappush(pqueuet, (vDataT[w]['ds'],w))

            if ( vDataS[w]['status'] == Status.scanned and
                 vDataS[w]['ds'] +vDataT[w]['ds'] < mu):
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


from graph.dijkstra import *
from graph.utility import *

from graph.astar import *
from graph.sample_graph import *

import matplotlib.pyplot as plt
import networkx as nx 
import matplotlib.cm as cm
import operator




def testShortestPathBasic(g,pos,src,dst,nodeSize):
    # networkx built-in function
    path0 = nx.shortest_path(g,src,dst,"weight")

    # dijkstra's
    (path1,vData1) = labeling(g,src,dst,"weight")

    # A*
    pi = potential_l2(g,dst)
    (path2,vData2)  = lowerBounding(g,src,dst,pi,
                                    "weight")    
    # bidirectional A*
    piRev = potential_l2(g.reverse(),src)
    (path3,vDataS,vDataT) = symmetricLowerBounding(g,src,dst,pi,piRev,"weight")
    
    print "dijkstra path len: ", len(path1)
    print "A* path len: ", len(path2)
    print "Bdr A* path len: ", len(path3)

    # visualize paths 
    plt.subplot(1,3,1) # draw all paths
    drawLargeGraph(g,pos,edgelists=[ toEdgeList(path1),toEdgeList(path2),toEdgeList(path3)],
                   sources=[path0[0]], sinks=[path0[-1]],nodesize=nodeSize)
    plt.subplot(1,3,2) # draw scanned nodes of A*
    scanned2 = [ v for v in g if vData2[v]['status'] == Status.scanned]
    print "# of scanned vertices in A*: " ,len(scanned2)
    drawLargeGraph(g,pos,nodelists=[scanned2],sources=[path0[0]],sinks=[path0[-1]],
                   nodesize=nodeSize)
    
    plt.subplot(1,3,3) # draw scanned nodes of bidirectional A*
    scannedS = [ v for v in g if vDataS[v]['status'] == Status.scanned]
    scannedT = [ v for v in g if vDataT[v]['status'] == Status.scanned]
    print "# of scanned vertices of bidirectional A*: ",\
        len(scannedS),"(forward), ",len(scannedT),"(backward), ",\
        len(set(scannedS).union(scannedT)),"(union)"
    drawLargeGraph(g,pos,nodelists=[scannedS,scannedT],
                   sources=[path0[0]],sinks=[path0[-1]],
                   nodesize=nodeSize)
    
    plt.show()
    

def demoRoadNetwork():

    (g,pos)  = loadCalGraph()
    
    src = 726 # 1800 
    dst = 17451 # 13621

    testShortestPathBasic(g,pos,src,dst,nodeSize=10)

    
def main():
    # test on a small graph
    (g,pos) = makeToyDiGraph()
    testShortestPathBasic(g,pos,1,11,nodeSize=60)
    
    # test on a medium size graph
    (g,pos) = makeRandomDiGraph()
    testShortestPathBasic(g,pos,7,29, nodeSize=40)
        
    # test on a road network
    demoRoadNetwork()
        
        
if __name__ == "__main__":
        main()


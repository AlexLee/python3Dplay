import scipy as sp
import math

import Basics
import mesh


def straighten(layer,mesh):
    #Changes all the edges in layer so that if the vector from a to b is regarded as forward, the inside of mesh is always to the left.
    newEdges = []
    for edge in layer:
        right = sp.cross(edge.dir[0],sp.array([0,0,1]))
        if mesh.contains(edge.a-0.01*right+0.5*edge.length*edge.dir[0]):
            newEdges.append(edge)
        else:
            newEdges.append(Basics.edge(edge.b,edge.a))
    return newEdges

def order(layer):
    activeEdge = layer[0]
    running = True
    output = [activeEdge]
    while running:
        startEdge = activeEdge
        for edge in layer:
            if sp.array_equal(edge.a,activeEdge.b):
                #If this edge starts at the end of the last edge
                output.append(edge)     #Add it to the order
                layer.remove(edge)      #Take it out of the old list
                activeEdge = edge       #Set it as the new last edge
            if startEdge==activeEdge:
                #There is no edge left in layer which starts at the end of activeEdge.
                #We've finished the layer
                running = False
    return output


#Function below attempts to handle layers with multiple loops. Nonfunctional.
##def order(layer):
##    running = True
##    activeEdge = layer[0]
##    activeLoop = [activeEdge]
##    loops = []
##    while running:
##        startEdge = activeEdge          #Save active Edge for later
##        for edge in layer:
##            if sp.array_equal(edge.a,activeEdge.b):
##                layer.remove(edge)
##                activeLoop.append(edge)
##                activeEdge = edge
##        if startEdge==activeEdge:
##            #We must not have found any.
##            loops.append(activeLoop)
##            activeLoop = [layer[0]]
##            layer = layer[1:]
##        if len(layer)==0: running = False
##    for loop in loops:
##        if not sp.array_equal(loop[0].a,loop[-1].b):
##            return 'Loop opening found at ' + str(loop[0].a)
##    return loops

def clean(layer):
    #Takes a straightened, ordered layer and turns any colinear edges with shared endpoints into single edges.
    print 'unimplemented'

def shell(shellCount,mesh,loopList,extrusionWidth):
    #This function takes a flat layer which has been linearized and generates the shell paths as edges.
    #WARNING: This function is really primitive, and should NOT be kept if this ever becomes more than a proof of concept program.
    loopGroups = []
    for loop in loopList:
        loopShells = []     #A list of the shells produced for this loop
        activeShell = loop    #A clean object to make sure I don't mess up my original borders.
        for shell in range(shellCount):
            #First we shift all the edges which compose the last shell inward by the proper amount
            if shell==0:
                for edge in activeShell:
                    #Only move the first shell in by half the width, so that its outer edge is correctly positioned.
                    edge.move(sp.cross(edge.dir[0]*extrusionWidth/2.0,sp.array([0,0,1])))
            else:
                for edge in activeShell:
                    edge.move(sp.cross(edge.dir[0]*extrusionWidth,sp.array([0,0,1])))
            #Then, for each edge, figure out where its direction vector intersects that of the one after it, and make that point its new B endpoint. This turns the shifted edges into a continuous loop again.
            for i in (len(activeshell)-1):
                       newB = activeShell[i].intersect(activeShell[i+1],True,False)
                       activeShell[i]=Basics.edge(activeShell[i].a,newB)
            activeShell[-1]=Basics.edge(activeShell[-1].a,activeShell[-1].intersect(activeShell[0],True,False))     #This line is sort of ugly, but it's just fixing the end of the last edge in the loop.
            loopShells.append(activeShell)
            #We let activeShell ride around, since we want the next loop to be shifted inward from this one, not from the beginning.
        #Once a loop has the correct number of shells, we throw them into loopGroups and move on.
        loopGroups.append(loopShells)
    return loopGroups
            

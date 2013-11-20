import scipy as sp
import numpy as np
import math
import Basics
import mesh


def straighten(layer,mesh):
    #Changes all the edges in layer so that if the vector from a to b is regarded as forward, the inside of mesh is always to the right.
    newEdges = []
    for edge in layer:
        right = sp.cross(edge.dir[0],sp.array([0,0,1]))
        if mesh.contains(edge.a+0.01*right+0.5*edge.length*edge.dir[0]):
            newEdges.append(edge)
        else:
            newEdges.append(Basics.edge(edge.b,edge.a))
    return newEdge


#Untested

def order(layer):
    running = True
    activeEdge = layer[0]
    activeLoop = [activeEdge]
    loops = []
    while running:
        startEdge = activeEdge          #Save active Edge for later
        for edge in layer:
            if sp.array_equal(edge.a,activeEdge.b):
                layer.remove(edge)
                activeLoop.append(edge)
                activeEdge = edge
        if startEdge==activeEdge:
            #We must not have found any.
            loops.append(activeLoop)
            activeLoop = [layer[0]]
            layer = layer[1:]
        if len(layer)==0: running = False
    return loops
            

def shell(shellCount,mesh,layer):
    #This function takes a flat layer which has been linearized and generates the shell paths.
    print 'foo'

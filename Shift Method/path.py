import scipy as sp
import Basics
import mesh
import layerClass


def straighten(layer, mesh):
    #Changes all the edges in layer so that if the vector from a to b is regarded as forward, the inside of mesh is always to the left.
    #layer is a list of edges outputted by mesh.chop. It is NOT a layer.
    newEdges = []
    for edge in layer:
        right = sp.cross(edge.dir[0],sp.array([0,0,1]))
        if mesh.contains(edge.a-0.01*right+0.5*edge.length*edge.dir[0]):
            newEdges.append(edge)
        else:
            newEdges.append(Basics.edge(edge.b,edge.a))
    return newEdges

def straightenAll(layerList):
    #Straightens the borders of all the layers in a list of layers.
    part = layerList[0].mesh
    for layer in layerList:
        layer.borders=straighten(layer.borders,part)

def order(layer):
    unsorted = layer
    activeEdge = unsorted[0]
    running = True
    output = []
    count = len(unsorted)-1
    loop = []
    while running:
        startCount = count
        for edge in unsorted[1:]:
            if sp.allclose(edge.a,activeEdge.b,1e-8,0):
                #If this edge starts at the end of the last edge
                loop.append(edge)     #Add it to the order
                unsorted.remove(edge)      #Take it out of the old list.
                activeEdge = edge       #Set it as the new last edge
                count -= 1
                break
        if count==startCount:
            print "Adding loop of length:" + str(len(loop))
            output.append(loop)
            loop =[]
        if count==0:
            print "Ending while. Current loop length:" + str(len(loop))
            output.append(loop)
            running = False
    return output

def clean(layer):
    #Takes a straightened, ordered layer and turns any colinear edges with shared endpoints into single edges.
    cleanLayer = []
    skip = False
    for index in range(len(layer)-1):
        if skip:
            skip=False
            continue
        e1 = layer[index]
        e2 = layer[index+1]
        if e1!='Loop end' and e2!='Loop end':
            if sp.allclose(e1.dir[0],e2.dir[0],1e-8,0):
                cleanLayer.append(Basics.edge(e1.a,e2.b))
                skip = True
            else:
                cleanLayer.append(e1)
    if layer[-1]!='Loop end':
        if not sp.allclose(layer[-1].b,cleanLayer[-1].b,1e-8,0):
            cleanLayer.append(layer[-1])
    return cleanLayer
                

def shell(shellCount,mesh,loopList,extrusionWidth):
    #This function takes a flat layer which has been straightened, ordered, and cleaned, then adds shells to it.
    #If input is [loop1,loop2,loop3] output is [loop1,shells of loop 1,loop 2, shells of loop 2,...]
    print "Not implemented woo!"

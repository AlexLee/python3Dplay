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

class section():
    #A contiguous list of edges, which can be open or closed.
    def __init__(self,startEdge):
        self.startEdge = startEdge
        self.edges = [startEdge]
        self.end = startEdge.b
        self.start = startEdge.a
    def __str__(self):
        return len(self.edges)
    def attempttoAdd(self,edge):
        #Attempts to add the edge to either end. updates self.start or end if it succeeds. Returns boolean for success.
        if sp.allclose(self.end,edge.a,1e-8,0):
            self.edges.append(edge)
            self.end = edge.b
            return True
        if sp.allclose(self.start,edge.b,1e-8,0):
            self.edges = [edge] + self.edges
            self.start = edge.a
            return True
        return False
    def checkClosed(self):
        #Checks if section is a closed loop.
        return sp.allclose(self.start,self.end,1e-8,0)
    def attempttoJoin(self,sect):
        #Tries to add sect, another section, to either end of self.
        if sp.allclose(self.end,sect.start,1e-8,0):
            self.edges.extend(sect.edges)
            self.end = sect.end
            return True
        if sp.allclose(self.start,sect.end,1e-8,0):
            self.edges = sect.edges + self.edges
            self.start = sect.start
            return True
        return False

def order(layer):
    #Sorts layer.borders into a list of loops. The loops are ordered such that each one touches its neighbors in the list index. Stores the output in layer.loops.
    segments = [section(layer.borders[0])]
    for edge in layer.borders[1:]:
        success = False
        for seg in segments:
            if seg.attempttoAdd(edge):
                success = True
                break
        if not success:
            segments.append(section(edge))
    while not allClosed(segments):
        for outerSeg in segments:
            for innerSeg in segments:
                if outerSeg.attempttoJoin(innerSeg):
                    segments.remove(innerSeg)
        allClosed(segments)
    layer.loops = [seg.edges for seg in segments]
    
    
    layer.loops = [seg.edges for seg in segments]
def allClosed(sections):
    #Checks if all the sections in sections, a list of section objects, are closed.
    for seg in sections:
        if not seg.checkClosed():
            return False
    return True
            
            
    
        
            

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

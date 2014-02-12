import scipy as sp
import Basics
import mesh
import layerClass


def straighten(layer):
    #Changes all the edges in layer so that if the vector from a to b is regarded as forward, the inside of mesh is always to the left.
    #layer is a list of edges outputted by mesh.chop. It is NOT a layer.
    newEdges = []
    for edge in layer.borders:
        right = sp.cross(edge.dir[0],sp.array([0,0,1]))
        if layer.mesh.contains(edge.a-0.01*right+0.5*edge.length*edge.dir[0]):
            newEdges.append(edge)
        else:
            newEdges.append(Basics.edge(edge.b,edge.a))
    layer.borders = newEdges

def straightenAll(layerList):
    #Straightens the borders of all the layers in a list of layers.
    for layer in layerList:
        straighten(layer)

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

def allClosed(sections):
    #Checks if all the sections in sections, a list of section objects, are closed.
    for seg in sections:
        if not seg.checkClosed():
            return False
    return True


def clean(layer):
    #Takes a straightened, ordered layer and turns any colinear edges with shared endpoints into single edges.
    #Outdated
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
                

def shell(shellCount,extrusionWidth,layer):
    #This function takes a layer which has been through straighten and order, and forms the perimeter lines which will actually be extruded from the loops.
    insets = [n*extrusionWidth+extrusionWidth/2.0 for n in range(shellCount)]
    shellGroups = []
    for loop in layer.loops:
        shells = []
        for inset in insets:
            shell = []
            for edge in loop:
                left = sp.cross(sp.array([0,0,1]),edge.dir[0])
                shell.append(Basics.edge(edge.a+left*inset,edge.b+left*inset))
            for index in range(len(shell)-1):
                activeEdge = shell[index]
                nextEdge = shell[index+1]
                if activeEdge.intersect(nextEdge,False,True):
                    intersect = activeEdge.intersect(nextEdge,True,True)
                    shell[index]=Basics.edge(activeEdge.a,intersect)
                    shell[index+1]=Basics.edge(intersect,nextEdge.b)
            activeEdge = shell[-1]
            nextEdge = shell[0]
            if activeEdge.intersect(nextEdge,False,True):
                intersect = activeEdge.intersect(nextEdge,True,True)
                shell[-1]=Basics.edge(activeEdge.a,intersect)
                shell[0]=Basics.edge(intersect,nextEdge.b)
            shells.append(shell)
        shellGroups.append(shells)
    return shellGroups
                

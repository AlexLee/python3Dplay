import scipy as sp
import Basics
import mesh
import layerClass
import surfaces

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
        if sp.allclose(self.end,edge.a):
            self.edges.append(edge)
            self.end = edge.b
            return True
        if sp.allclose(self.start,edge.b):
            self.edges = [edge] + self.edges
            self.start = edge.a
            return True
        return False
    def checkClosed(self):
        #Checks if section is a closed loop.
        return sp.allclose(self.start,self.end)
    def attempttoJoin(self,sect):
        #Tries to add sect, another section, to either end of self.
        if sp.allclose(self.end,sect.start):
            self.edges.extend(sect.edges)
            self.end = sect.end
            return True
        if sp.allclose(self.start,sect.end):
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

def clean(loop):
    '''
    Takes a straightened, ordered loop and cleans it up by removing any colinear edges with shared endpoints which can be represented as single edges. Returns a straight ordered loop with such substitions made.

    NOTE FOR NEXT WORK: This appproach makes the handling of the first/last edge interface ugly. Rewrite to save chains as pairs of start and end indices, and not combine anything until all edges have been checked and no chains can
    be further extended.
    '''
    chain = False
    startChain = None
    cleanLoop = []
    nextIndex = range(len(loop))[1:]+[0]
    for i in range(len(loop)):
        #Look at edge i and edge i+1
        act = loop[i]
        nex = loop[nextIndex[i]]
        if sp.allclose(act.dir[0],nex.dir[0]):
            #As this is an ordered loop, we know they share endpoints. Thus if they share dirs these two edges can be replaced by a single one.
            if not chain:
                #chain flag remembers whether act can form a single edge with one or more edges before it in the loop.
                #If chain is false, we're starting a new chain of replaceable edges and need to remember where it starts.
                startChain = act
            chain = True
        elif chain:
            #If act and nex can't chain together, we've reached the end of any chain we may be in, and should add it to the output.
            chain = False
            cleanLoop.append(Basics.edge(startChain.a,act.b))
        else:
            #If we don't have an active chain going, we need to put act into the output as is, since it can't chain with either of its neighbors.
            cleanLoop.append(act)
    #handle the hanging stuff from the end of the loop
    if chain:
        #If at the end of the for loop the chain flag is still raised, the first edge in loop can be combined with the last edge, and potentially more before it.
        #Also, the first edge in cleanLoop is guaranteed to have the same dir and startpoint as the first edge in loop. Therefore, if chain, we should combine the first edge in cleanLoop with the active chain.
        cleanLoop.append(Basics.edge(startChain.a,cleanLoop[0].b))
        cleanLoop = cleanLoop[1:]
    return cleanLoop

def cleanLayer(layer):
    #Clean all the loops in layer.loops.
    cleanLoops = []
    for loop in layer.loops:
        cleanLoops.append(clean(loop))
    layer.loops = cleanLoops
        
def shell(shellCount,extrusionWidth,layer):
    '''
    This function takes a layer which has been through straighten and order, and forms the perimeter lines which will actually be extruded from the loops.
    Stores perimeter lines in layer.shells as a list of shell groups. Each shell group is a list of shells with varying insets. Shells are ordered lists of edges similar to loops.
    '''
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
                if activeEdge.check2dintersect(nextEdge):
                    intersect = activeEdge.point2dIntersect(nextEdge)
                    shell[index]=Basics.edge(activeEdge.a,intersect)
                    shell[index+1]=Basics.edge(intersect,nextEdge.b)
            activeEdge = shell[-1]
            nextEdge = shell[0]
            if activeEdge.check2dintersect(nextEdge):
                intersect = activeEdge.point2dIntersect(nextEdge)
                shell[-1]=Basics.edge(activeEdge.a,intersect)
                shell[0]=Basics.edge(intersect,nextEdge.b)
            shells.append(shell)
        shellGroups.append(shells)
    layer.shells = shellGroups

def wrapLayer(layer,surface,n):
    '''
    Performs surface.edgeWrap on all edges in surface.shells. Needs expanding to full paths once I'm generating those. n is number of interpolation segments per edge.
    '''
    newGroups = []
    for shellGroup in layer.shells:
        newGroup = []
        for shell in shellGroup:
            newShell = []
            for edge in shell:
                newShell.extend(surface.edgeWrap(edge,n))
            newGroup.append(newShell)
        newGroups.append(newGroup)
    layer.shells = newGroups

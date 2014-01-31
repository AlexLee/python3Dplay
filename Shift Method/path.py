import scipy as sp
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
    #This function currently cannot handle multiple loops.
    activeEdge = layer[0]
    running = True
    output = [activeEdge]
    count = len(layer)-1
    loop = 1
    while running:
        startCount = count
        for edge in layer:
            if sp.allclose(edge.a,activeEdge.b,1e-8,0):
                #If this edge starts at the end of the last edge
                output.append(edge)     #Add it to the order
                layer.remove(edge)      #Take it out of the old list.
                activeEdge = edge       #Set it as the new last edge
                count -= 1
                break
        if count==startCount:
            output.extend('Loop end',layer[0])
            loop +=1
        if count==0:
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
            

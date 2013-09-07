#The error reports in this are extremely hackish so far. I'll implement actual error classes if this gets built into something bigger. If this comment makes it into something bigger, make fun of me for it.

from Basics import *

def stl_import(fileName):
    #Imports an ASCII stl file coontaining ONE solid model.
    output=None #Holding variable for the output mesh object
    currentTris = [] #list of tris which have been created but not yet included into a solid.
    currentPoints=[] #list of points which have been created but not yet included in a tri
    currentNormal=None #Holding variable for one normal vector which has not yet been included in a tri.
    inMesh = None #Boolean flag to ensure currentTris isn't populated outside a mesh.
    inTri = False #Boolean flag to ensure currentPoints isn't populated outside a tri
    stl=open(fileName,'r')
    for line in stl:
        #Terminating a tri resets currentPoints, currentNormal, and stores the tri in currentTris
        lineList = line.split()
        if lineList[0]=='endfacet':
            if not inTri:
                print "Error: endfacet found outside of tri."
                return
            currentTris.append(tri(currentPoints,currentNormal))
            currentPoints=[]
            currentNormal=[]
            inTri=False
            continue
        if lineList[0]=='endloop':continue #I don't understand why loops exist.
        #Ending a mesh
        if lineList[0]=='endsolid':
            if not inMesh:
                print "Error: endsolid found outside of mesh."
                return
            inMesh=False
            output=mesh(currentTris)
            continue
        #Initiating a new mesh
        if lineList[0]=='solid':
            if inMesh:
                print "Error: solid initiated inside another solid."
                return            
            inMesh=True
            continue
        #Initiating a new triangle wipes all old points and stores the normal vector
        if lineList[0]=='facet':
            if inTri:
                print "Error: facet initiated inside another facet."
                return
            inTri=True
            currentNormal=vector(lineList[2],lineList[3],lineList[4])
            continue
        if lineList[0]=='outer': continue #I don't understand why loops exist.
        #Put vertices into currentPoints list
        if lineList[0]=='vertex':
            if len(currentPoints)>2:
                print "Error, nontriangle facet in file."
                return
            currentPoints.append(point(lineList[1],lineList[2],lineList[3]))
            continue
    if output!=None:
        return output
    else:
        print "Error: endsolid not found!"
        return


testPoint = point(8,8,8)
testVector = vector(0,0,50,testPoint)
            

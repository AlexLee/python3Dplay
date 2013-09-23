import Basics
import math
import scipy as sp

#Completed
def box(mins,maxes):
    #defines a box mesh by its minimum and maximum values.
    a=sp.array([mins[0],mins[1],mins[2]])
    b=sp.array([mins[0],maxes[1],mins[2]])
    c=sp.array([maxes[0],maxes[1],mins[2]])
    d=sp.array([maxes[0],mins[1],mins[2]])
    e=sp.array([mins[0],mins[1],maxes[2]])
    f=sp.array([mins[0],maxes[1],maxes[2]])
    g=sp.array([maxes[0],maxes[1],maxes[2]])
    h=sp.array([maxes[0],mins[1],maxes[2]])
    return Basics.mesh([
        #Bottom
        Basics.tri([a,b,c]),
        Basics.tri([a,d,c]),            
        #Top
        Basics.tri([e,f,g]),
        Basics.tri([e,h,g]),
        #Front Left
        Basics.tri([d,c,g]),
        Basics.tri([d,h,g]),
        #Front Right
        Basics.tri([b,c,g]),
        Basics.tri([b,f,g]),
        #Back Left
        Basics.tri([a,d,h]),
        Basics.tri([a,e,h]),
        #Back Right
        Basics.tri([a,b,f]),
        Basics.tri([a,e,f])])

class boxRegion:
    #A bounding box object meant to nest within itself to quickly define large regions as inside or outside a mesh. 
    def __init__(self,mesh,xMin,yMin,zMin,xMax,yMax,zMax,depth=0,maxDepth=1):
        self.mesh = mesh #Stores the mesh which this box is used to study.
        self.xMax=float(xMax)
        self.xMin=float(xMin)
        self.yMax=float(yMax)
        self.yMin=float(yMin)
        self.zMax=float(zMax)
        self.zMin=float(zMin)
        self.xLen = abs(self.xMax-self.xMin)
        self.yLen = abs(self.yMax-self.yMin)
        self.zLen = abs(self.zMax-self.zMin)
        self.box = box([xMin,yMin,zMin],[xMax,yMax,zMax]) #Mesh box around boxregion, to be used in checking edges.
        self.center = sp.array([(self.xMax+self.xMin)/2,(self.yMax+self.yMin)/2,(self.zMax+self.zMin)/2])
        self.solid = None #This flag states whether the region is homogenous. 
        self.inside = None #This flag states whether the region is inside or outside a mesh.
        self.depth = depth #This counts how many boxRegions self is nested within.
        self.maxDepth = maxDepth
        self.children = []

    def __str__(self):
        return 'x: ' + str(self.xMin)+'-'+str(self.xMax)+' y: ' + str(self.yMin)+'-'+str(self.yMax)+' z: ' + str(self.zMin)+'-'+str(self.zMax)

    def contains(self,p):
        #Checks if point p is within self. This does not change self.solid, self.inside or self.children. Completed.
        return self.xMin<p[0]<=self.xMax and self.yMin<p[1]<=self.yMax and self.zMin<p[2]<=self.zMax
        return False

    def checkEdges(self):
        #This function has been simplified to make sure it doesn't cause any trouble. To be optimized again later by reintroducing self.edges. Checks if the region is anything other than wholly inside or wholly outside self.mesh.
        for edge in self.mesh.edges:
            if self.contains(edge.a) or self.contains(edge.b):
                #One end of the edge is inside therefore an edge is either wholly inside the region or enters the region through a side.
                self.solid=False
                return
            if self.box.edge_intersect(edge):
                #If we get to this stage, no points are inside. Thus we're only testing for edges that go all the way through the region without ending.
                self.solid=False
                return
        self.solid=True
        return            

    def checkInside(self):
        #Returns self.inside unless self.solid is False, in which case it prints for now. Sophisticated error management comes later.
        if not self.solid: self.checkEdges()
        if not self.solid:
            self.inside = 'Not Homogeneous'
            return self.inside
        self.inside = self.mesh.contains(self.center)
        return self.inside

    def split(self,axis):
        #Split along the given axis.
        if axis=='major':
            lens = [self.xLen,self.yLen,self.zLen]
            if self.xLen==max(lens):                
                    self.split(0)
                    return
            if self.yLen==max(lens):
                    self.split(1)
                    return
            if self.zLen==max(lens):
                    self.split(2)
                    return
        elif axis==0:
            xMid = (self.xMax+self.xMin)/2
            childA = boxRegion(self.mesh, self.xMin, self.yMin, self.zMin, xMid, self.yMax, self.zMax, self.depth+1, self.maxDepth)
            childB = boxRegion(self.mesh, xMid, self.yMin, self.zMin, self.xMax, self.yMax, self.zMax, self.depth+1, self.maxDepth)
        elif axis==1:
            yMid = (self.yMax+self.yMin)/2
            childA = boxRegion(self.mesh, self.xMin, self.yMin, self.zMin, self.xMax, yMid, self.zMax, self.depth+1, self.maxDepth)
            childB = boxRegion(self.mesh, self.xMin, yMid, self.zMin, self.xMax, self.yMax, self.zMax, self.depth+1, self.maxDepth)
        elif axis==2:
            zMid = (self.zMax+self.zMin)/2
            childA = boxRegion(self.mesh, self.xMin, self.yMin, self.zMin, self.xMax, self.yMax, zMid, self.depth+1, self.maxDepth)
            childB = boxRegion(self.mesh, self.xMin, self.yMin, zMid, self.xMax, self.yMax, self.zMax, self.depth+1, self.maxDepth)
        self.children=[childA,childB]

    def tesselate(self):
        #Splits all nonsolid regions which do not yet have children. Effectively makes the tree one level deeper. Will not exceed maxdepth.
        self.checkEdges()
        if self.depth<self.maxDepth:
            if not self.solid:
                if self.children==[]:
                    self.split('major') #Split along the longest axis.
                else:
                    for child in self.children:
                        child.tesselate()

    def getBottom(self):
        #Returns the bottom most region objects in the tree. The sum of these objects will be self.
        output = []
        if self.children==[]: return [self]
        for child in self.children:
            if child.children==[]: output.append(child)
            else:
                for c in child.children:
                    carrier = c.getBottom()
                    for i in carrier:
                        output.append(i)
        return output

    def completeTree(self):
        for i in range(self.maxDepth):
            self.tesselate()
        if self.children==[]:
            self.checkInside()
            return
        for child in self.children:
            if child.children==[]:
                child.checkInside()
            else:
                child.completeTree()
        

    def volume(self):
        #returns the volume of the region
        return self.xLen*self.yLen*self.zLen

    def getRegion(self,p):
        #Finds the lowest region in the tree which contains p. Returns self if no children containing p exist.
        if not self.contains(p): return 'point not in region'
        output = self
        for c in self.children:
            if c.contains(p):
                output = c.getRegion(p)
        return output
                


MeshA = box([0,0,0],[5,5,5])
#testBox = boxRegion(MeshA,0,0,0,20,20,20,0,6)

tb = boxRegion(MeshA,0,0,0,20,20,20,0,6)
tb.completeTree()


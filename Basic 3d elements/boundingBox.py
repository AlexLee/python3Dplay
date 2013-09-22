from Basics import *

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
    return mesh([
        #Bottom
        tri([a,b,c]),
        tri([a,d,c]),            
        #Top
        tri([e,f,g]),
        tri([e,h,g]),
        #Front Left
        tri([d,c,g]),
        tri([d,h,g]),
        #Front Right
        tri([b,c,g]),
        tri([b,f,g]),
        #Back Left
        tri([a,d,h]),
        tri([a,e,h]),
        #Back Right
        tri([a,b,f]),
        tri([a,e,f])])

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
        self.edges = [] #This list contains all edges which can or do interact with 
        self.solid = None #This flag states whether the region is homogenous. 
        self.inside = None #This flag states whether the region is inside or outside a mesh.
        self.depth = depth #This counts how many boxRegions self is nested within.
        self.maxDepth = maxDepth
        self.children = []
    def __str__(self):
        return str(self.xMin) + ' ' + str(self.yMin) + ' ' + str(self.zMin) + ' ' + str(self.xMax) + ' ' + str(self.yMax) + ' ' + str(self.zMax)
    def contains(self,p):
        #Checks if point p is within self. This does not change self.solid, self.inside or self.children. Completed.
        return self.xMin<=p[0]<=self.xMax and self.yMin<=p[1]<=self.yMax and self.zMin<=p[2]<=self.zMax
    def checkPoints(self,m):
        #Checks if mesh m has any points inside self. Sets self.solid to false if there are any. Completed.
        for point in m.points:
            if self.contains(point):
                self.solid=False
                return True
        return False
    def checkEdges(self,m=None):
        #If m is not None, this function checks m.edges and populates self.edges with any edges that interact with self. Otherwise, it only checks edges in self.edges. This allows child boxes to inherit self.edges and thus
        #not recheck edges that their parent already eliminated. self.solid is flipped by 
        if m!= None:
            self.edges = []
            output = False
            for edge in m.edges:
                #Only 3 cases: Not inside, traverses a side, and wholly inside. Checking one point tests for wholly inside, and the edge_intersect tests whether the edge traverses a side.
                if self.contains(edge.a):
                    self.edges.append(edge)
                    self.solid=False
                elif self.box.edge_intersect(e):
                    self.edges.append(edge)
                    self.solid=False
        else:
            oldEdges = self.edges
            self.edges = []
            for edge in oldEdges:
                if self.contains(edge.a):
                    self.edges.append(edge)
                    self.solid=False
                elif self.box.edge_intersect(e):
                    self.edges.append(edge)
                    self.solid=False
    def checkInside(self,m):
        #Returns self.inside unless self.solid is False, in which case it prints for now. Sophisticated error management comes later.
        if not self.solid: print "Region not homogeneous, unclear if inside or outside."
        elif self.inside != None: return self.inside
        else:
            return m.contains(self.senter)
    def tesselate(self):
        #Splits all nonsolid regions which do not yet have children. Effectively makes the tree one level deeper. Will not exceed maxdepth.
        self.checkEdges(self.mesh)
        if not self.solid:
            if self.depth<self.maxDepth:
                if self.children==[]:
                    xMid = (self.xMax+self.xMin)/2
                    yMid = (self.yMax+self.yMin)/2
                    zMid = (self.zMax+self.zMin)/2
                    childA = boxRegion(self.mesh, self.xMin, self.yMin, self.zMin, xMid, yMid, zMid, self.depth+1, self.maxDepth)
                    childB = boxRegion(self.mesh, xMid, yMid, zMid, self.xMax, self.yMax, self.zMax, self.depth+1, self.maxDepth)
                    self.children=[childA,childB]
                else:
                    for child in self.children:
                        child.tesselate()


testMesh = box([0,0,0],[15,15,15])
testBox = boxRegion(testMesh,0,0,0,20,20,20)

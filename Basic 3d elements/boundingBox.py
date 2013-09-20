from Basics import *

def box(mins,maxes):
    #defines a box by its minimum and maximum values.
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
    #A bounding box object meant to nest within itself to quickly define large regions as inside or outside a model. 
    def __init__(self,xMax,yMax,zMax,xMin,yMin,zMin,depth=0):
        self.xMax=float(xMax)
        self.xMin=float(xMin)
        self.yMax=float(yMax)
        self.yMin=float(yMin)
        self.zMax=float(zMax)
        self.zMin=float(zMin)
        self.xLen = abs(self.xMax-self.xMin)
        self.yLen = abs(self.yMax-self.yMin)
        self.zLen = abs(self.zMax-self.zMin)
        self.mesh = box([xMin,yMin,zMin],[xMax,yMax,zMax])
        self.center = sp.array([(self.xMax+self.xMin)/2,(self.Ymax+self.yMin)/2,(self.zMax+self.Zmin)/2])
        self.edges = []
        self.solid = True #This flag states whether the region is homogenous. 
        self.inside = False #This flag states whether the region is inside or outside a mesh.
        self.depth = depth #This counts how many boxRegions self is nested within.
        self.sections = []
    def contains(self,p):
        #Checks if point p is within self. This does not change self.solid, self.inside or self.sections.
        return self.xMin<=p[0]<=self.xMax and self.yMin<=p[1]<=self.yMax and self.zMin<=p[2]<=self.zMax
    def checkPoints(self,m):
        #Checks if mesh m has any points inside self. Sets self.solid to false if there are any.
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
                elif self.mesh.edge_intersect(e):
                    self.edges.append(edge)
                    self.solid=False
        else:
            oldEdges = self.edges
            self.edges = []
            for edge in oldEdges:
                if self.contains(edge.a):
                    self.edges.append(edge)
                    self.solid=False
                elif self.mesh.edge_intersect(e):
                    self.edges.append(edge)
                    self.solid=False



#This file is incomplete but I'm pushing anyway before going to the gym. The plan is to just make mesh boxes for all the bounding boxes to perform checkEdges.

#The overall plan is to write a function in slice.py which takes the mesh, draws a boxRegion over its extents, then subdivides that boxRegion until all subdivisions are either homogenous (self.solid = True) or at the max depth which
#you include in the input to said function. Then whole areas of layers can just be declared solid or empty without having to do a bunch more checks on crazy complicated meshes. Also, I'm going to add a list of edges which interact with
#a given boxRegion, since if an edge doesn't interact with a region, no child regions will interact with it either. Just need to work out how to recognize edges that are inside but don't cross in an efficient manner.
        

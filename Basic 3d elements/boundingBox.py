from Basics import *

class box(mesh):
    #A handy subclass of mesh to make box meshes quicker.
    def __init__

class boxRegion:
    #A bounding box object meant to nest within itself to quickly define large regions as inside or outside a model. 
    def __init__(self,xMax,yMax,zMax,xMin,yMin,zMin):
        self.xMax=float(xMax)
        self.xMin=float(xMin)
        self.yMax=float(yMax)
        self.yMin=float(yMin)
        self.zMax=float(zMax)
        self.zMin=float(zMin)
        self.xLen = abs(self.xMax-self.xMin)
        self.yLen = abs(self.yMax-self.yMin)
        self.zLen = abs(self.zMax-self.zMin)
        self.center = sp.array([(self.xMax+self.xMin)/2,(self.Ymax+self.yMin)/2,(self.zMax+self.Zmin)/2])
        self.solid = True #This flag states whether the region is homogenous. 
        self.inside = False #This flag states whether the region is inside or outside a mesh.
        self.depth = 0 #This counts how many boxRegions self is nested within.
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
    def checkEdges(self,m):
        #Checks if mesh m has any edges which in any way traverse the region. Sets self.solid to false if there are any.

#This file is incomplete but I'm pushing anyway before going to the gym. The plan is to just make mesh boxes for all the bounding boxes to perform checkEdges.

#The overall plan is to write a function in slice.py which takes the mesh, draws a boxRegion over its extents, then subdivides that boxRegion until all subdivisions are either homogenous (self.solid = True) or at the max depth which
#you include in the input to said function. Then whole areas of layers can just be declared solid or empty without having to do a bunch more checks on crazy complicated meshes. Also, I'm going to add a list of edges which interact with
#a given boxRegion, since if an edge doesn't interact with a region, no child regions will interact with it either. Just need to work out how to recognize edges that are inside but don't cross in an efficient manner.
        

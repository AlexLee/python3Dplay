import Basics
import scipy as sp
import layerClass


class mesh:
    def __init__(self,tris):
        self.tris = tris
        self.points = []
        self.edges = []
        for tri in self.tris:
            for point in tri.points:
                self.points.append(point)
            for edge in tri.edges:
                self.edges.append(edge)
        self.region = sp.array([[0,0,0],[0,0,0]])
        self.center = None
        self.updateLims()
    def __str__(self):
        string = ''
        for tri in self.tris:
            string=string+' [' + str(tri) + ']'
        return string
    def updateLims(self):
        xSum = 0 
        ySum = 0
        zSum = 0
        for pointA in self.points:
            xSum += float(pointA[0])
            ySum += float(pointA[1])
            zSum += float(pointA[2])
            self.region[0][0]=float(max(self.region[0][0],pointA[0]))
            self.region[1][0]=float(min(self.region[1][0],pointA[0]))
            self.region[0][1]=float(max(self.region[0][1],pointA[1]))
            self.region[1][1]=float(min(self.region[1][1],pointA[1]))
            self.region[0][2]=float(max(self.region[0][2],pointA[2]))
            self.region[1][2]=float(min(self.region[1][2],pointA[2]))            
        pointCount = len(self.points)
        self.center = sp.array([xSum/pointCount,ySum/pointCount,zSum/pointCount]) #Center of all points in the mesh, useful for some optimizations.
    def vector_intersect(self,v):
        for tri in self.tris:
            if tri.vector_intersect(v):
                return tri.vector_intersect(v,True)
        return False
    def edge_intersect(self,e):
        #Checks if edge e collides with any triangles in self.
        for tri in self.tris:
            if tri.edge_intersect(e): return True
        return False
    def contains(self,p):
        #Checks whether point is inside self.
        if not self.region[1][0]<=p[0]<=self.region[0][0]: return False #Simple bounding box check
        if not self.region[1][1]<=p[1]<=self.region[0][1]: return False
        if not self.region[1][2]<=p[2]<=self.region[0][2]: return False
        testVector = sp.array([[0,0,50+self.region[0][2]],p])
        inside = False
        for tri in self.tris:
            if tri.vector_intersect(testVector): inside = not inside
        return inside
    def chop(self,layerHeight):
        #Returns an ordered list of layers. Each layer consists of a list of edges which represent the intersection of self with the plane z=(layer #-1/2) * layerHeight. The first item in each layer is a point inside the mesh.
        height = self.region[0][2]-self.region[1][2]
        layers= []
        for layer in range(int(height/layerHeight)):
            #Adding 0.5*layerHeight to height of cutting plane so that the plane will be as representative as possible of the general layer volume.
            cuttingPlane = Basics.plane(sp.array([0,0,(layer+0.5)*layerHeight]),sp.array([[0,0,1],[0,0,0]]))
            edges = []
            for tri in self.tris:
                intersect = tri.plane_intersect(cuttingPlane)
                if type(intersect)!=type(False):
                    edges.append(intersect)
            layers.append(layerClass.layer(edges,layerHeight,self))
        return layers
                    

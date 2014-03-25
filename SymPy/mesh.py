import Basics
import scipy as sp


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
        Xs = [point[0] for point in self.points]
        Ys = [point[1] for point in self.points]
        Zs = [point[2] for point in self.points]
        self.region[0][0]=[[max(Xs),max(Ys),max(Zs)],[min(Xs),min(Ys),min(Zs)]]
        pointCount = len(self.points)
        self.center = [sum[l] for l in [Xs,Ys,Zs]]/pointCount #Center of all vertices in the mesh, useful for some optimizations.
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
        testVector = sp.array([[0,0,50+self.region[0][2]],p])
        inside = False
        for tri in self.tris:
            if tri.vector_intersect(testVector): inside = not inside
        return inside
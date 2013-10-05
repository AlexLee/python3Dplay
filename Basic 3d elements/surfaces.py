import Basics
import boundingBox
import math
import scipy as sp
import numpy as np

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
        self.xMax=0 #Max and mins on each axis provide useful optimizations.
        self.xMin=0
        self.yMax=0
        self.yMin=0
        self.zMax=0
        self.zMin=0
        xSum = 0 #Sums are used to calculate center
        ySum = 0
        zSum = 0
        for pointA in self.points:
            xSum += float(pointA[0])
            ySum += float(pointA[1])
            zSum += float(pointA[2])
            self.xMax=float(max(self.xMax,pointA[0]))
            self.xMin=float(min(self.xMin,pointA[0]))
            self.yMax=float(max(self.yMax,pointA[1]))
            self.yMin=float(min(self.yMin,pointA[1]))
            self.zMax=float(max(self.zMax,pointA[2]))
            self.zMin=float(min(self.zMin,pointA[2]))            
        pointCount = len(self.points)
        self.center = sp.array([xSum/pointCount,ySum/pointCount,zSum/pointCount]) #Center of all points in the mesh, useful for some optimizations.
        self.tree = None
    def formRegions(self):
        self.tree = boxRegion(self,self.xMin,self.xMax,self.yMin,self.yMax,self.zMin,self.zMax,0,6)
        self.tree.finalize(self)

class openMesh(mesh):
    #Defines a collection of tris which is an open surface.
    def __init__(self,tris):
        mesh.__init__(self,tris)
    def above(self,p):
        #Checks if point p is below the surface
        if p[0]<self.zMin: return True
        testVector = sp.array([[0,0,5000],p])
        for tri in self.tris:
            if tri.vector_intersect(testVector): return True
        return False
    def edge_intersect(self,e):
        #Checks if edge e collides with any triangles in self.
        for tri in self.tris:
            if tri.edge_intersect(e): return True
        return False
    

class closedMesh(mesh):
    #Defines a collection of tris which is a closed surface.
    def __init__(self,tris):
        mesh.__init__(self,tris)
    def contains(self,p):
        #Checks whether point is inside self.
        if not self.xMin<=p[0]<=self.xMax: return False #Simple bounding box check
        if not self.yMin<=p[1]<=self.yMax: return False
        if not self.zMin<=p[2]<=self.zMax: return False
        testVector = sp.array([[0,0,50+self.zMax],p])
        hits = 0
        for tri in self.tris:
            if tri.vector_intersect(testVector): hits+=1
        return hits%2==1
    def edge_intersect(self,e):
        #Checks if edge e collides with any triangles in self.
        for tri in self.tris:
            if tri.edge_intersect(e): return True
        return False
        

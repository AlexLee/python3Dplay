import scipy as sp
import numpy as np
import math
#Points are 3x1 matrices, vectors are 3x2. Row 2 of vectors are their origin points. Below are the 3 unit vectors.
vi = sp.array([[1,0,0],[0,0,0]])
vj = sp.array([[0,1,0],[0,0,0]])
vk = sp.array([[0,0,1],[0,0,0]])

def unit(vector):
    #Takes a vector and returns its unit vector with origin preserved.
    if vector.shape==(2, 3):
        return sp.array([vector[0]/sp.sqrt(vector[0].dot(vector[0])),vector[1]])
    elif vector.shape==(3,): return sp.array([vector/sp.sqrt(vector.dot(vector))])
    

class edge:
    #Stores a pair of points and defines a connection between them.
    def __init__(self,a,b):
        self.a=a
        self.b=b
    def length(self):
        #Returns the length of the edge.
        subtrArray = sp.dstack([self.a,-self.b]).sum(2)
        return sp.sqrt(sp.sum([n**2 for n in subtrArray]))
    def parallel(self,other):
        #Checks if self is parallel to another edge other. Returns a boolean.
        return self.getDir()==other.getDir()
    def getDir(self):
        #Returns a positive unit vector, a to b or b to a. x/(x dot x)^0.5 produces the unit vector of x.
        d=sp.array([abs(self.b[0] - self.a[0]),abs(self.b[1] - self.a[1]),abs(self.b[2] - self.a[2])])
        return sp.array([unit(d),[0,0,0]])
        
        
    
class tri:
    #Stores a triangle. Normal is defined as a vector aka a 3x2 array. Triangle is formed from an ordered list of 3 connected points aka 3x1 arrays.
    def __init__(self,points,normal=None):
        #Normal should be a single vector. Points should be a list of points.
        self.points = sp.array(points)
        if normal !=None:
            self.normal = unit(normal)
        else:
            va = sp.array([ self.points[0][0]-self.points[1][0], self.points[0][1]-self.points[1][1], self.points[0][2]-self.points[1][2]])
            vb = sp.array([ self.points[0][0]-self.points[2][0], self.points[0][1]-self.points[2][1], self.points[0][2]-self.points[2][2]])
            self.normal = unit(sp.array([np.cross(va,vb),[0,0,0]]))
        self.plane = plane(self.points[0],self.normal)
        #Create edges through the list of points. the first edge goes from self.points[0] to self.points[1] and the last from self.points[-1] to self.points[0]
        self.edges = []
        for i in range(3):
            #Very silly and intentionally pythonic way to do this.
            self.edges.append(edge(self.points[i],self.points[i-2]))        
    def __str__(self):
        return str(self.points[0]) + " , " + str(self.points[1]) + " , " + str(self.points[2])
    def perimeter(self):
        #Return the perimeter of the facet
        perim = 0
        for edge in self.edges:
            perim+= edge.length()
        return perim
    def area(self):
        #Utilises Heron's formula
        p = self.perimeter()/2.0
        a = self.edges[0].length()
        b = self.edges[1].length()
        c = self.edges[2].length()
        return (p*(p-a)*(p-b)*(p-c))**0.5
    def vector_intersect(self,vector_in,coords=False):
        #Checks if the vector intersects self.plane, then tests whether the point is inside tri. Coords decides whether a boolean or a point object is returned.
        intersect = self.plane.vector_intersect(vector_in,True)
        if type(intersect)==type(False): return False
        else:
            #point is inside tri iff ABxAP.unit==BCxBP.unit==CAxCP.unit
            #Defining points just to make it neater. 
            p1 = self.points[0]
            p2 = self.points[1]
            p3 = self.points[2]
            #Define the 6 vectors
            AB=sp.array([ p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2]])
            BC=sp.array([ p2[0]-p3[0], p2[1]-p3[1], p2[2]-p3[2]])
            CA=sp.array([ p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]])
            AP=sp.array([ p1[0]-intersect[0], p1[1]-intersect[1], p1[2]-intersect[2]])
            BP=sp.array([ p2[0]-intersect[0], p2[1]-intersect[1], p2[2]-intersect[2]])
            CP=sp.array([ p3[0]-intersect[0], p3[1]-intersect[1], p3[2]-intersect[2]])
            #Find cross products
            c1 = unit(sp.cross(AB,AP))
            c2 = unit(sp.cross(BC,BP))
            c3 = unit(sp.cross(CA,CP))
            if not coords: return np.array_equal(c1,c2) and np.array_equal(c1,c3)
            else: return intersect
    def plane_intersect(self,p):
        #Returns an edge in both plane p and self or boolean False if edge DNE.
        #A triangle which is in a plane produces only vectors in the plane, and the vector_intersect method on planes does not count vectors in the plane, thus points will only ever have length 2.
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]
        #Transforming the 3 sides into vectors for testing against the plane
        sides=[sp.array([ p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2]]), sp.array([ p2[0]-p3[0], p2[1]-p3[1], p2[2]-p3[2]]), sp.array([ p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]])]
        points=[]
        for side in sides:
            intersect=p.vector_intersect(side,True)
            if intersect!=False:
                points+=intersect
        if points==[]:return False
        return edge(points[0],points[1])
        



class plane:
    #Defines a plane from a point and a normal.
    def __init__(self,point,normal):
        self.origin = point
        self.normal = unit(normal)
    def vector_intersect(self,v,coords=False):
        #Tests whether a vector v hits self
        if self.normal[0].dot(v[0])==0: return False
        #dot product includes cos(angle between 2 vectors) therefore if the angle between 2 vectors is >90 dot product is negative. So a negative dot-prod signals an obtuse angle between 2 vectors.
        #So if we were only trying to detect hits to the "back" of the plane, we could toss out any vectors whose dot with the normal is negative. However we don't care which side we're hitting, so we use self.origin-v[1] as
        #a vector known to hit from the same side as v. In this way if the signs of the 2 dot products are different, we know that v does not hit.
        #I still haven't wrapped my head around how the parameter is also the scalar multiple necessary to make v reach the plane.
        parameter = self.normal[0].dot(self.origin-v[1])/self.normal[0].dot(v[0])
        if coords:
            if parameter>=0: return v[1]+(v[0]*parameter)
        elif parameter>=0: return True
        return False
        

class mesh:
    #Defines a collection of tris which is ideally a closed surface.
    def __init__(self,tris):
        self.tris = tris
        self.points = []
        self.edges = []
        for tri in self.tris:
            for point in tri.points:
                self.points.append(point)
            for edge in tri.edges:
                self.edges.append(edge)
        xSum = 0 #Sums are used to calculate center
        ySum = 0
        zSum = 0
        self.xMax=0 #Max and mins on each axis provide useful optimizations.
        self.xMin=0
        self.yMax=0
        self.yMin=0
        self.zMax=0
        self.zMin=0
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
    def contains(self,p):
        #Checks whether point is inside self.
        if not self.xMin<=p[0]<=self.xMax: return False #Simple bounding box check
        if not self.yMin<=p[1]<=self.yMax: return False
        if not self.zMin<=p[2]<=self.zMax: return False
        testVector = sp.array([[0,0,50+self.zMax],p])
        hits = 0
        for tri in self.tris:
            if tri.vector_intersect(testVector): hits+=1
        if hits%2==1: return True
        return False

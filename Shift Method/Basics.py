import scipy as sp
import numpy as np
import math

#Points are 3x1 matrices, vectors are 3x2. Row 2 of vectors are their origin points. Below are the 3 unit vectors.
vi = sp.array([[1,0,0],[0,0,0]])
vj = sp.array([[0,1,0],[0,0,0]])
vk = sp.array([[0,0,1],[0,0,0]])

def unit(vector):
    #Takes a vector and returns its unit vector with origin preserved. If vector lacks an origin, no origin is added.
    if vector.shape==(2, 3):
        return sp.array([vector[0]/math.sqrt(vector[0].dot(vector[0])),vector[1]])
    elif vector.shape==(3,):
        dot = vector.dot(vector)
        if dot==0: return vector
        return vector/math.sqrt(dot)

def distance(a,b):
    #Returns the distance from point a to point b. Takes any iterable class of length 3 representing X,Y,Z in cartesian coordinates. Arrays/lists/tuples all work.
    subtrArray = sp.dstack([a,-b]).sum(2)
    return sp.sqrt(sp.sum([n**2 for n in subtrArray]))

def vlength(v):
    #Returns the length of vector v.
    return sp.sqrt(sp.sum([n**2 for n in v]))

class edge:
    #Stores a pair of points and defines a connection between them.
    def __init__(self,a,b):
        self.a=a
        self.b=b
        self.dir=None
        self.setDir()
        subtrArray = sp.dstack([self.a,-self.b]).sum(2)
        self.length = sp.sqrt(sp.sum([n**2 for n in subtrArray])) 
    def __str__(self):
        return str(self.a)+str(self.b)
    def parallel(self,e):
        #Checks if self is parallel to another edge e. Returns a boolean.
        return (sp.cross(self.dir[0],e.dir[0])==0).all()
    def move(self,v):
        #Moves the edge by vector v.
        if v.shape==(2,3):
            self.a = self.a + v[0]
            self.b = self.b +v[0]
        else:
            self.a = self.a + v
            self.b = self.b +v
    def setDir(self):
        #Updates self.dir.      
            d=sp.array([self.b[0] - self.a[0],self.b[1] - self.a[1],self.b[2] - self.a[2]])
            self.dir = sp.vstack((unit(d),self.a))
    def containsPoint(self,p):
        #Checks if p is on edge
        AP = sp.array(p-self.a)
        BP = sp.array(p-self.b)
        if not ((0==sp.cross(AP,BP)).all(): return False
        return vlength(AP)<=self.length and vlength(BP)<=self.length
    def colinear(self,e):
        #Checks if self is colinear with e.
        return (0==sp.cross(self.dir[0],e.dir[0])).all() and (0==sp.cross(self.dir[0],sp.array(self.a-e.a))).all()
    def intersect(self,e,coords=True):
        AA = sp.array(e.a-self.a)
        proj = np.dot(self.dir[0],AA)*unit(self.dir[0])
        point = sp.array(self.a+proj)
        if self.containsPoint(point) and e.containsPoint(point): return point
        return False

#Cleaned above this point

class tri:
    #Stores a triangle. Normal is defined as a vector aka a 3x2 array. Triangle is formed from an ordered list of 3 connected points aka 3x1 arrays.
    def __init__(self,points,normal=None):
        #Normal should be a single vector. Points should be a list of points.
        self.points = sp.array(points)
        if normal !=None:
            self.normal = unit(normal)
        else:
            ab = sp.array([ self.points[0][0]-self.points[1][0], self.points[0][1]-self.points[1][1], self.points[0][2]-self.points[1][2]])
            ac = sp.array([ self.points[0][0]-self.points[2][0], self.points[0][1]-self.points[2][1], self.points[0][2]-self.points[2][2]])
            self.normal = unit(sp.array([np.cross(ab,ac),[0,0,0]]))
        self.plane = plane(self.points[0],self.normal)
        #Create edges through the list of points. the first edge goes from self.points[0] to self.points[1] and the last from self.points[-1] to self.points[0]
        self.edges = []
        for i in range(3):
            #Very silly and intentionally pythonic way to do this.
            self.edges.append(edge(self.points[i],self.points[i-2]))        
    def __str__(self):
        return str(self.points[0]) + " , " + str(self.points[1]) + " , " + str(self.points[2])
    def move(self,v):
        #Moves the triangle by vector v.
        updatedpoints = []
        for edge in self.edges:
            edge.move(v)
            updatedpoints.append(edge.a)
        self.points = updatedpoints
        self.plane = plane(self.points[0],self.normal)
    def warp(self,surface):
        #surface is an open mesh with a zMin of 0 that also has only one z value per xy coordinate.
        newpoints = []
        for point in self.points:
            print 'foo'
    def perimeter(self):
        #Return the perimeter of the facet
        perim = 0
        for edge in self.edges:
            perim+= edge.length
        return perim
    def area(self):
        #Utilises Heron's formula
        p = self.perimeter()/2.0
        a = self.edges[0].length
        b = self.edges[1].length
        c = self.edges[2].length
        return (p*(p-a)*(p-b)*(p-c))**0.5
    def vector_intersect(self,vector_in,coords=False):
        #Checks if the vector intersects self.plane, then tests whether the point is inside tri. Coords decides whether a boolean or a point object is returned.
        intersect = self.plane.vector_intersect(vector_in,True)
        if type(intersect)==type(False): return False
        else:
            if self.contains(intersect):
                if coords: return intersect
                return True
            return False
    def contains(self,p):
        #Checks whether a point is on self.
        #point is inside tri iff ABxAP.unit==BCxBP.unit==CAxCP.unit
            #Defining points just to make it neater. 
            p1 = self.points[0]
            p2 = self.points[1]
            p3 = self.points[2]
            #Define the 6 vectors
            AB=sp.array([ p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2]])
            BC=sp.array([ p2[0]-p3[0], p2[1]-p3[1], p2[2]-p3[2]])
            CA=sp.array([ p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]])
            AP=sp.array([ p1[0]-p[0], p1[1]-p[1], p1[2]-p[2]])
            BP=sp.array([ p2[0]-p[0], p2[1]-p[1], p2[2]-p[2]])
            CP=sp.array([ p3[0]-p[0], p3[1]-p[1], p3[2]-p[2]])
            #Find cross products
            c1 = unit(sp.cross(AB,AP))
            c2 = unit(sp.cross(BC,BP))
            c3 = unit(sp.cross(CA,CP))
            return np.array_equal(c1,c2) and np.array_equal(c1,c3)
        
    def edge_intersect(self,e):
        #Returns whether an edge hits self.
        intersect = self.vector_intersect(e.dir(),True)
        if type(intersect)==type(False): return False
        return distance(intersect,e.a)<e.length
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
    def tri_intersect(self,t):
        #Returns an edge in both self and t.
        pEdge = plane_intersect(t.plane)
        intersects = []
        for edge in t.edges:
            if pEdge.intersects(edge,False):
                intersects.append(pEdge.intersects(edge,True))
        if len(intersects)==0:
            #If there are no intersections between the edges of tri and the edge formed by the plane intersect, the original plane intersect is on the surface of tri and therefore equivalent to
            #tri intersect.
            return pEdge
        if len(intersects)==1:
            #If there is 1 intersection, one end of pEdge will still be in tri. So we check if pEdge.a is in tri, and if it is return an edge from it to the 1 intersect. Otherwise we do the same to B
            point  = intersects[0]
            if self.contains(pEdge.a):
                return edge(pEdge.a,point)
            return edge(pEdge.b,point)
        if len(intersects)==2:
            #If there are 2 intersections, pEdge.a and pEdge.b both lie outside Tri, and the intersection of the triangles goes from one edge of t to the other. Thus it is the edge from one intersect
            #to the other
            return edge(intersects[0],intersects[1])
            
            
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



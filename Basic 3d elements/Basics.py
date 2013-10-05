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
        return sp.array([vector[0]/math.sqrt(vector[0].dot(vector[0])),vector[1]])
    elif vector.shape==(3,):
        dot = vector.dot(vector)
        if dot==0: return vector
        return vector/math.sqrt(dot)

def distance(a,b):
    #Returns the distance from point a to point b
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)

class edge:
    #Stores a pair of points and defines a connection between them.
    def __init__(self,a,b):
        self.a=a
        self.b=b
        self.vector = self.getDir()
    def __str__(self):
        return str(self.a)+str(self.b)
    def length(self):
        #Returns the length of the edge.
        subtrArray = sp.dstack([self.a,-self.b]).sum(2)
        return sp.sqrt(sp.sum([n**2 for n in subtrArray]))
    def parallel(self,e):
        #Checks if self is parallel to another edge e. Returns a boolean.
        d1 = self.getDir()
        d2 = e.getDir()
        c=np.cross(d1,d2)
        return c[0][0]**2 + c[0][1]**2 + c[0][2]**2==0
    def getDir(self):
        #Returns a unit vector, a to b.
        d=sp.array([self.b[0] - self.a[0],self.b[1] - self.a[1],self.b[2] - self.a[2]])
        return sp.vstack((unit(d),[0,0,0]))
    def containsPoint(p):
        #Checks if p is on edge
        return distance(p,self.a)+distance(p,self.b)==self.length()
    def colinear(self,e):
        #Returns boolean whether self is colinear with e
        if not self.parallel(e): return False
        scalarX=None
        scalarY=None
        scalarZ=None
        if self.vector[0][0]!=0:
            scalarX = (e.a[0]-self.a[0])/self.vector[0][0]
        if self.vector[0][1]!=0:
            scalarY = (e.a[1]-self.a[1])/self.vector[0][1]
        if self.vector[0][2]!=0:
            scalarZ = (e.a[2]-self.a[2])/self.vector[0][2]
        prev=None
        for s in (scalarX,scalarY,scalarZ):
            if s!=None:
                if prev==None:
                    prev=s
                else:
                    if prev!=s:
                        return False
                    prev=s
        return True
    def intersect(self,e,coords=True):
        #Returns the point of intersection of self with another edge, or false if it doesn't intersect.
        if self.length()==0 or e.length()==0: return 'Error 0 length edge'
        if self.parallel(e):
            if not self.colinear(e):
                return False
            else:
                AC = distance(self.a,e.a)
                AD = distance(self.a,e.b)
                BC = distance(self.b,e.a)
                BD = distance(self.b,e.b)
                if AC==0 or AD ==0: return self.a
                if BC==0 or BD==0: return self.b
                for d in (AC,AD,BC,BD):
                    for c in (AC,AD,BC,BD):
                        if d+c in (AC,AD,BC,BD):
                            return 'coincident along a segment'
                return False
        p1 = self.a
        p2 = e.a
        v1 = self.vector
        v2 = e.vector
        s=(p1[1]-p2[1]+v1[0][1]*(p1[2]+p2[2])/v1[0][2])/(v2[0][1]-v1[0][1]*v2[0][2]/v1[0][2])
        t = (p2[2]+v2[0][2]*s-p1[2])/v1[0][2]
        if p1[0]+v1[0][0]*t==p2[0]+v2[0][0]*s:
            point = p1+v1[0]*t
        else: return False
        if max(distance(point,self.a),distance(point,self.b))>self.length() or max(distance(point,e.a),distance(point,e.b))>e.length():
            return False
        else:
            if coords: return point
            else: return True
            
        
    
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
        intersect = self.vector_intersect(e.getDir(),True)
        if type(intersect)==type(False): return False
        return distance(intersect,e.a)<e.length()
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



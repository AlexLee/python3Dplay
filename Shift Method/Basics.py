import scipy as sp
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
    if v.shape==(2, 3):
        return sp.sqrt(sp.sum([n**2 for n in v[0]]))
    else:
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
    def __eq__(self,e):
        return sp.array_equal(e.a,self.a) and sp.array_equal(e.b,self.b)
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
        if not ((0==sp.cross(AP,BP)).all()): return False
        return vlength(AP)<=self.length and vlength(BP)<=self.length
    def colinear(self,e):
        #Checks if self is colinear with e.
        return (0==sp.cross(self.dir[0],e.dir[0])).all() and (0==sp.cross(self.dir[0],sp.array(self.a-e.a))).all()
    def check2dintersect(self,e):
        #Check if the two edges intersect in 2d. Ignores Z.
        p = self.a[:2]
        q = e.a[:2]
        r = (self.b-self.a)[:2]
        s = (e.b-e.a)[:2]
        if sp.cross(r,s)==0: return False
        t=sp.cross(q-p,s)/sp.cross(r,s)
        u = sp.cross(q-p,r)/sp.cross(r,s)
        if t>=0 and t<=1 and u>=0 and u<=1:
            return True
        return False
    def point2dIntersect(self,e):
        #Return the 2d intersection of the two edges. Intersection is placed at the same z as self.a
        p = self.a[:2]
        q = e.a[:2]
        r = (self.b-self.a)[:2]
        s = (e.b-e.a)[:2]
        t=sp.cross(q-p,s)/sp.cross(r,s)
        u = sp.cross(q-p,r)/sp.cross(r,s)
        if t>=0 and t<=1 and u>=0 and u<=1:
            intersect = p+t*r
            return sp.array([intersect[0],intersect[1],self.a[2]])
        return None
    def intersect(self,e,coords=True,actual=True):
        #Returns data about the intersection of self and edge e.
        #if coords, return the intersection as a point or false if intersection DNE. If not coords, return true/false
        #actual is a boolean for whether the intersection must be on both edges or not. 
        AA = sp.array(e.a-self.a)
        proj = sp.dot(self.dir[0],AA)*unit(self.dir[0])
        point = sp.array(self.a+proj)   #One issue with this method is in case of parallel edges, it returns a rather arbitrary point on self.
        if actual:
            #Here the parallels are solved because the erroneous intersections won't be on both lines.
            if self.containsPoint(point) and e.containsPoint(point): 
                if coords: return point
                return True
            return False
        else:
            #Here we have to check that the point is at least colinear with both.
            EAP = sp.array(point-e.a)
            EBP = sp.array(point-e.b)
            SAP = sp.array(point-self.a)
            SBP = sp.array(point-self.b)
            s1 = EAP[0]/EBP[0]
            s2 = SAP[0]/EBP[0]
            if sp.allclose(EAP/EBP,s1,1e-8,0) and sp.allclose(SAP/SBP,s2,1e-8,0):
                if coords: return point
                return True
            return False
    def equivalent(self,e):
        #Checks if e shares both endpoints with self.
        return (sp.array_equal(self.a,e.a) and sp.array_equal(self.b,e.b)) or (sp.array_equal(self.a,e.b) and sp.array_equal(self.b,e.a))

class tri:
    #Stores a triangle. Normal is defined as a vector aka a 3x2 array. Triangle is formed from an ordered list of 3 connected points aka 3x1 arrays.
    def __init__(self,points):
        #Points should be a list of 3x1 arrays.
        self.points = sp.array(points)
        #Create edges through the list of points.
        self.edges = []
        for i in range(3):
            #Silly and intentionally pythonic way to do this. Edges are 1-2, 2-3, 3-1.
            self.edges.append(edge(self.points[i],self.points[i-2]))
        self.normal = unit(sp.array([sp.cross(self.edges[0].dir[0],self.edges[1].dir[0]),[0,0,0]]))
        self.plane = plane(self.points[0],self.normal)                
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
    def perimeter(self):
        #Return the perimeter of the triangle
        return (sum(edge.length for edge in self.edges))
    def area(self):
        #Utilises Heron's formula
        p = self.perimeter()/2.0
        return (p*(p-self.edges[0].length)*(p-self.edges[1].length)*(p-self.edges[2].length))**0.5    
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
            return sp.array_equal(c1,c2) and sp.array_equal(c1,c3)
    def edge_intersect(self,e):
        #Returns whether an edge hits self.
        intersect = self.vector_intersect(e.dir(),True)
        if type(intersect)==type(False): return False
        return distance(intersect,e.a)<e.length and distance(intersect,e.b)<e.length
    def plane_intersect(self,p):
        #Returns a list of an edge and 
        #A triangle which is in a plane produces only vectors in the plane, and the vector_intersect method on planes does not count vectors in the plane, thus points will only ever have length 2.
        sides=[self.edges[0].dir,self.edges[1].dir,self.edges[2].dir]
        points=[]
        for side in sides:
            intersect=p.vector_intersect(side,True)
            if type(intersect)!=type(False):
                points.append(intersect)
        if points==[]:return (False,0)
        if len(points)==1: return (points[0],1)
        return (edge(points[0],points[1]),2)
    def centroid(self):
        #Return the centroid of the triangle
        return (self.points[0] + self.points[1] + self.points[2])/3
    def tesselate(self):
        #Returns 3 triangles composed of selfs vertices and selfs centroid. This is a really crappy way to tesselate. The original edges are preserved and not broken up.
        p = self.points
        c = self.centroid()
        return [tri([p[0],p[1],c]),tri([p[0],p[2],c]),tri([p[1],p[2],c])]
    
##I don't think I have a need for this function anymore, but I'm keeping it in case I do. Also I'm not sure I ever tested this very well.

##    def tri_intersect(self,t):
##        #Returns an edge in both self and t.
##        pEdge = self.plane_intersect(t.plane)
##        intersects = []
##        for edge in t.edges:
##            if pEdge.intersects(edge,False):
##                intersects.append(pEdge.intersects(edge,True))
##        if len(intersects)==0:
##            #If there are no intersections between the edges of tri and the edge formed by the plane intersect, the original plane intersect is on the surface of tri and therefore equivalent to
##            #tri intersect.
##            return pEdge
##        if len(intersects)==1:
##            #If there is 1 intersection, one end of pEdge will still be in tri. So we check if pEdge.a is in tri, and if it is return an edge from it to the 1 intersect. Otherwise we do the same to B
##            point  = intersects[0]
##            if self.contains(pEdge.a):
##                return edge(pEdge.a,point)
##            return edge(pEdge.b,point)
##        if len(intersects)==2:
##            #If there are 2 intersections, pEdge.a and pEdge.b both lie outside Tri, and the intersection of the triangles goes from one edge of t to the other. Thus it is the edge from one intersect
##            #to the other
##            return edge(intersects[0],intersects[1])
##            
            
class plane:
    #Defines a plane from a point and a normal.
    def __init__(self,point,normal):
        self.origin = point
        self.normal = unit(normal)
    def vector_intersect(self,v,coords=False):
        #Tests whether a vector v hits self
        if (self.normal[0].dot(v[0])==0).all(): return False
        #Dot product includes cos(angle between 2 vectors) therefore if the angle between 2 vectors is >90 dot product is negative. A negative dot-prod signals an obtuse angle between 2 vectors.
        #So if we were only trying to detect hits to the "back" of the plane, we could toss out any vectors whose dot with the normal is negative. However we don't care which side we're hitting, and some obtuse angles will still hit,
        #so we use (plane origin - vector origin) as a vector known to hit from the same side as v. In this way if the signs of the 2 dot products are different, we know that v does not hit.
        if v.shape==(2, 3):
            dotProd = self.normal[0].dot(v[0])
            if dotProd==0:
                parameter = self.normal[0].dot(self.origin-v[1])
            else:
                parameter = self.normal[0].dot(self.origin-v[1])/self.normal[0].dot(v[0])
        elif v.shape==(3,):
            return 'Attempted to intersect a vector of shape [3,]. Without starting point, intersects are meaningless.'
        if coords:
            if parameter>=0: return v[1]+(v[0]*parameter)
        elif parameter>=0: return True
        return False



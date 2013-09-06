class point:
    #Stores a point in 3 space
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def __str__(self):
        #returns the coordinates of self as a str of format x,y,z
        return str(self.x)+","+str(self.y)+","+str(self.z)
    def dist(self,other):
        #Other is another point. Returns distance between other and self as a float.
        return float(((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)**0.5)
    def __sub__(self,other):
        #Returns a vector from other (a point) to self
        return vector(self.x-other.x,self.y-other.y,self.z-other.z)
    def __add__(self,vector):
        #Returns a point found by adding vector to self's position.
        return point(self.x+vector.x,self.y+vector.y,self.z+vector.z)
    

class vector:
    #Stores a vector and will later provide vector mathematics, maybe.
    def __init__(self,x,y,z,origin=point(0,0,0)):
        self.x=float(x)
        self.y=float(y)
        self.z=float(z)
        self.origin=origin
    def __add__(self,other):
        #Implements vector addition. other must be a vector.
        return vector(self.x+other.x,self.y+other.y,self.z+other.z)
    def __sub__(self,other):
        #Implements vector addition. other must be a vector.
        return vector(self.x-other.x,self.y-other.y,self.z-other.z)
    def __neg__(self):
        return vector(-self.x,-self.y,-self.z)
    def __div__(self,c):
        #Implements the / operator as scalar division.
        return vector(self.x/c,self.y/c,self.z/c)
    def __mul__(self,c):
        #Implements the * operator as scalar multiplication
        return vector(self.x*c,self.y*c,self.z*c)
    def length(self):
        #Returns length of the vector
        return ((self.x)**2+(self.y)**2+(self.z)**2)**0.5
    def unit(self):
        #Returns the unit vector of self
        return self/self.length()
    def __str__(self):
        #Returns the vector in notation [x,y,z]
        return "["+str(self.x)+","+str(self.y)+","+str(self.z)+"]"
    def __eq__(self,other):
        #Checks whether self is equal to another vector in magnitude and direction. Returns a boolean.
        return self.x==other.x and self.y==other.y and self.z==other.z
    def parallel(self,other):
        #Checks whether self is equal to another vector in direction and ignores magnitude. Returns a boolean.
        return self.unit()==other.unit()
    def cross(self,other):
        #Implements cross product operations on self and another vector.
        return vector(self.y*other.z-self.z*other.y,self.x*other.z-self.z*other.x,self.x*other.y-self.y*other.x)
    def dot(self,other):
        #Implements dot product operations on self and another vector.
        return self.x*other.x+self.y*other.y+self.z*other.z

class edge:
    #Stores a pair of points and defines a connection between them.
    def __init__(self,a,b):
        self.a=a
        self.b=b
    def length(self):
        #Returns the length of the edge
        return ((self.a.x-self.b.x)**2+(self.a.y-self.b.y)**2+(self.a.z-self.b.z)**2)**0.5
    def parallel(self,other):
        #Checks if self is parallel to another edge other. Returns a boolean.
        return self.getDir()==other.getDir()
    def getDir(self):
        #Returns a positive unit vector, a to b or b to a.
        x = abs(self.b.x - self.a.x)
        y = abs(self.b.y - self.a.y)
        z = abs(self.b.z - self.a.z)
        return vector(x,y,z).unit()
        
        
    
class tri:
    #Stores a triangle. Normal is defined as a vector. Triangle is formed from an ordered list of 3 connected points.
    def __init__(self,points,normal=None):
        #Normal should be a single vector. Points should be a list of points.
        self.points = points
        if normal !=None:
            self.normal = normal.unit() #Normals don't need to be anything other than unit vectors.
        else:
            p1 = points[0]
            p2 = points[1]
            p3 = points[3]
            va = vector(p1.x-p2.x,p1.y-p2.y,p1.z-p2.z)
            vb = vector(p1.x-p3.x,p1.y-p3.y,p1.z-p3.z)
            value = va.cross(vb)
            self.normal = product.unit()
        self.plane = plane(self.points[0],self.normal)
        self.edges = []
        #Create edges through the list of points. the first edge goes from self.points[0] to self.points[1] and the last from self.points[-1] to self.points[0]
        pointA = self.points[0]
        iteratingPoints = self.points[1:]
        iteratingPoints.append(self.points[0])
        for point in iteratingPoints:
            pointB = point
            self.edges.append(edge(pointA,pointB))
            pointA = point
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
  

class plane:
    #Defines a plane from a point and a normal.
    def __init__(self,point,normal):
        self.origin = point
        self.normal = normal.unit()
    def vector_intersect(self,vector,coords=False):
        if self.normal.dot(vector)==0: return False
        parameter = self.normal.dot(self.origin-vector.origin)/self.normal.dot(vector)
        if coords:
            if parameter>=0: return vector.origin+(vector*parameter)
        elif parameter>=0: return True
        return False

            
            
                




vector1 = vector(0,0,5,point(0,0,2))
plane1 = plane(point(50,5,3),vector(0,0,1))

##p1 = point(0,0,0)
##p2 = point(0,0,3)
##p3=point(3,4,0)
##e1 = edge(p1,p2)
##e2 = edge(p2,p1)
##e3 = edge(p1,p3)
##n1 = vector(0,0,1)
##v1 = vector(0,1,0)
##f1 = tri([p1,p2,p3],n1)

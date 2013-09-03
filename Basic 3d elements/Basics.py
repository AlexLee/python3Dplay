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
    

class vector:
    #Stores a vector and will later provide vector mathematics, maybe.
    def __init__(self,x,y,z):
        self.x=float(x)
        self.y=float(y)
        self.z=float(z)
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

class edge:
    #Stores a pair of points and defines a connection between them.
    def __init__(self,a,b):
        self.a=a
        self.b=b
    def length(self):
        #Returns the length of the edge
        return ((self.a.x-self.b.x)**2+(self.a.y-self.b.y)**2+(self.a.z-self.b.z)**2)**0.5
    def intersects(self,other):
        #Other is another edge. Checks if other intersects with self. Sharing endpoints does not qualify as intersection. Returns boolean.
        sanityCheck = self.a.dist(other.a) or self.a.dist(other.b) or self.b.dist(other.a) or self.b.dist(other.b)<self.length() #If the length of self cannot reach either end of other, they cannot intersect.
        if not sanityCheck or self.parallel(other): return False
    def parallel(self,other):
        #Checks if self is parallel to another edge other. Returns a boolean.
        return self.getDir()==other.getDir()
    def getDir(self):
        #Returns a positive unit vector, a to b or b to a.
        x = abs(self.b.x - self.a.x)
        y = abs(self.b.y - self.a.y)
        z = abs(self.b.z - self.a.z)
        return vector(x,y,z).unit()
        
        
    
class facet:
    #Stores a flat polygon which is theoretically always a triangle. Normal is defined as a vector. Polygon is formed from an ordered list of connected points.
    def __init__(self,points,normal):
        #Normal should be a single vector. Points should be a list of points.
        self.points = points
        self.normal = normal.unit() #Normals don't need to be anything other than unit vectors.
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
        if len(self.edges)==3:
            #Utilises Heron's formula
            p = self.perimeter()/2.0
            a = self.edges[0].length()
            b = self.edges[1].length()
            c = self.edges[2].length()
            return (p*(p-a)*(p-b)*(p-c))**0.5
        





p1 = point(0,0,0)
p2 = point(0,0,3)
p3=point(3,4,0)
e1 = edge(p1,p2)
e2 = edge(p2,p1)
e3 = edge(p1,p3)
n1 = vector(0,0,5)
v1 = vector(0,0,5)
f1 = facet([p1,p2,p3],n1)

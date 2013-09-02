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
        return ((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)**0.5
    

class vector:
    #Stores a vector and will later provide vector mathematics, maybe.
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

class edge:
    #Stores a pair of points and defines a connection between them.
    def __init__(self,a,b):
        self.a=a
        self.b=b
    def __len__(self):
        return ((a.x-b.x)**2+(a.y-b.y)**2+(a.z-b.z)**2)**0.5
    def intersects(self,other):
        #Other is another edge. Checks if other interacts with self. Returns boolean.
        
    
class facet:
    #Stores a flat polygon which is theoretically always a triangle. Normal is defined as a vector. Polygon is formed from an ordered list of connected points.
    def __init__(self,points,normal)
        #Normal should be a single vector. Points should be a list of points.
        self.points = points
        self.normal = normal
        self.edges = []

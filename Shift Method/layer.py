import Basics

class layer(loops,thickness,mesh):
    #Layer object created by mesh.chop function, and acted on by lots of stuff.
    #loops is a list of closed loops of edges. This is the outermost edge, not an actual path.
    #thickness is the vertical thickness of the layer.
    #mesh is the mesh which the layer was created from.
    def __init__(self,borders,thickness,mesh):
        self.borders = borders
        self.thickness = thickness
        self.mesh = mesh
        #Domain of the mesh. Maxes in [0], mins in [1]
        self.domain = sp.array([self.mesh.region[0][0:2],self.mesh.region[1][0:2]])
        #A list of all the 
        self.extrusions = []
        self.path = []

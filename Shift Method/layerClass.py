import Basics
import scipy as sp

class layer():
    '''
    Layer object created by mesh.chop function, and acted on by lots of stuff.
    Thickness is the vertical thickness of the layer.
    Mesh is the mesh which the layer was created from.
    Borders is the output of mesh.chop.
    '''
    def __init__(self,borders,thickness,mesh):
        #The outline of the shape in the layer. This is not an actual extrusion path as it is on the surface itself, not inset for extrusion width.
        self.borders = borders
        #Vertical thickness of the layer
        self.thickness = thickness
        #Reference to the mesh which created this layer.
        self.mesh = mesh
        #Domain of the mesh. Maxes in [0], mins in [1]
        self.domain = sp.array([self.mesh.region[0][0:2],self.mesh.region[1][0:2]])
        #A list of all the extrusions in the path.
        self.extrusions = []
        #The final list of movements to be exported as gcode. Includes travels.
        self.path = []
        self.loops = None
        self.shells = []

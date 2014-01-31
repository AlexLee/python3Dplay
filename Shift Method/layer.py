class layer(loops,thickness,mesh):
    #Layer object created by mesh.chop function, and acted on by lots of stuff.
    #loops is a list of closed loops of edges. This is the outermost edge, not an actual path.
    #thickness is the vertical thickness of the layer.
    #mesh is the mesh which the layer was created from.
    def __init__(self,loops,thickness,mesh):
        self.loops = loops
        self.thickness = thickness
        self.mesh = mesh
        
        

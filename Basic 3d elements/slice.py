import Basics
import stl_importer
import boundingBox


class layer:
    def __init__(self,surface):
        self.surface = surface
        self.edges = []
    def addEdge(self,edge):
        self.edges.append(edge)


def sliceToEdges(model,surface,layerHeight):
    #This function outputs a list of layers. Layers are 
    layers = []
    currentEdges = []


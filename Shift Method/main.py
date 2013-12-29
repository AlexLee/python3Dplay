#This may or may not be where the actual main program ends up. For now it just imports everything so i can test.
import scipy as sp
import math

import display
import Basics
import stl_importer
import mesh
import surfaces
import path
import gcode_Exporter

test = stl_importer.stl_import('model.stl')
layers = test.chop(1.5)
straightLayers = []
for layer in layers:
    straightLayers.append(path.straighten(layer,test))
orderedLayers = []
for layer in straightLayers:
    orderedLayers.append(path.order(layer))
display.edgePlot(layers[2])
display.edgePlot(straightLayers[2])

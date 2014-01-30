#This may or may not be where the actual main program ends up. For now it just imports everything so i can test.
import scipy as sp
import math

import display
import Basics
import stl_importer
import mesh
import path
import gcode_Exporter

test = stl_importer.stl_import('model.stl')
layers = test.chop(1)
stLayers = []
for layer in layers:
    stLayers.append(path.straighten(layer,test))
#display.edgePlot(stLayers[3])
#order1 = path.order(stLayers[3])
oLayers = []
for layer in stLayers:
    oLayers.append(path.order(layer))

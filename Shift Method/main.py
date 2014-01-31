#This may or may not be where the actual main program ends up. For now it just imports everything so i can test.
import scipy as sp
import display
import stl_importer
import path
import gcode_Exporter

test = stl_importer.stl_import('model.stl')
layers = test.chop(0.2)
stLayers = []
for layer in layers:
    stLayers.append(path.straighten(layer,test))
#display.edgePlot(stLayers[3])
#order1 = path.order(stLayers[3])
oLayers = []
for layer in stLayers:
    oLayers.append(path.order(layer)

#This may or may not be where the actual main program ends up. For now it just imports everything so i can test.
import scipy as sp
import display
import stl_importer
import path
import gcode_Exporter

test = stl_importer.stl_import('twoLoop.stl')
layers = test.chop(1)
path.straighten(layers[-2])
path.order(layers[-2])
shellList = path.shell(3,0.25,layers[-2])

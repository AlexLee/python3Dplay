#This may or may not be where the actual main program ends up. For now it just imports everything so i can test.
import scipy as sp
import display
import stl_importer
import path
import surfaces
#import mesh

w1 = surfaces.wave(5,8,0,0)
test = stl_importer.stl_import('model.stl')
test = test.tesselate(1)
test = w1.meshShift(test,-1)
layers = test.chop(.5)
##path.straighten(layers[3])
##path.order(layers[3])

##for layer in layers:
##    path.straighten(layer)
##    path.order(layer)
##    path.cleanLayer(layer)
##    path.shell(3,0.75,layer)
##    path.wrapLayer(layer,w1,4)

chain = []
for layer in layers:
    chain.extend(layer.borders)
display.edgePlot(chain)

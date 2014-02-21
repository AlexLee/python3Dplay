#This may or may not be where the actual main program ends up. For now it just imports everything so i can test.
import scipy as sp
import display
import stl_importer
import path
import surfaces
#import mesh

w1 = surfaces.wave(1.5,20,0,0)
test = stl_importer.stl_import('model.stl')
m1 = test.tesselate(1)
#m1 = w1.meshShift(m1,-1)
##layers = test.chop(2)
##for layer in layers:
##    path.straighten(layer)
##    path.order(layer)
##    path.cleanLayer(layer)
##    path.shell(3,0.75,layer)
##    path.wrapLayer(layer,w1,8)
##chain = []
##for layer in layers:
##    for a in layer.shells:
##        for b in a:
##            chain.extend(b)
##display.edgePlot(chain)


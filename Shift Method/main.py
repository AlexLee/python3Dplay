#This may or may not be where the actual main program ends up. For now it just imports everything so i can test.
import scipy as sp
import display
import stl_importer
import path
import surfaces
#import mesh

w1 = surfaces.wave(5,30,0,0)
test = stl_importer.stl_import('model.stl')
#test = test.tesselate(2)
#test = w1.meshShift(test,-1)
layers = test.chop(3)
layers = layers[:-1]
for layer in layers:
    path.straighten(layer)
    path.order(layer)
    path.shell(3,0.75,layer)
    path.wrapLayer(layer,w1,4)


chain = []
for layer in layers:
    for shellGroup in layer.shells:
        for shell in shellGroup:
            chain.extend(shell)
display.edgePlot(chain)

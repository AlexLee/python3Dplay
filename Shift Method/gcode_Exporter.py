import scipy as sp
import numpy as np
import Basics
import math
import surfaces

travelSpeed = 100
printSpeed = 50

def gcode_Export(path,e):
    #Converts a list of vectors to a gcode file for the path. e is the scalar relating E coordinates to distance moved. 
    #Outputs gcode to the file output.gcode, with the file start.gcode at the beginning and end.gcode at the end.
    output = open('output.gcode','w')
    start = open('start.gcode','r')
    end = open('end.gcode','r')
    for line in start:
        output.write(line)
    output.write(G1([path[0][1][0],path[0][1][1],path[0][1][2],0]) + '\n')
    ePos = 0
    for v in path:
        ePos +=e*Basics.vlength(v[0])
        output.write(G1(v[0]+v[1],ePos) + '\n')
    for line in end:
        output.write(line)
    

def G1(p,e=0):
       #Returns a gcode of the form G1 X(p[0]) Y(p[1]) Z(p[2]) E(e)
    return 'G1 X'+str(p[0]) + ' Y' + str(p[1]) + ' Z' + str(p[2])+ ' E' + str(e)


w1 = surfaces.wave(1,1,0,0)
v1 = sp.array([[0,2,0],[0.08,0,0]])
gcode_Export(w1.vectorWrap(v1,0.1),1)



#Currently not functional pending some changes to earlier parts of the code.

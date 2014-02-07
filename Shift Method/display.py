import scipy as sp
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import Basics

def display(path):
    #Displays path, a series of length 3 iterables representing points in 3d cartesian space.
    print path[0]
    Xs = [point[0] for point in path]
    Ys = [point[1] for point in path]
    Zs = [point[2] for point in path]
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.plot(Xs,Ys,Zs)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

def edgePlot(path):
    #Displays path, a series of edge objects.
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    plt.xlabel('X')
    plt.ylabel('Y')
    for n in range(len(path)):
        edge = path[n]
        ax.plot([edge.a[0],edge.b[0]],[edge.a[1],edge.b[1]],[edge.a[2],edge.b[2]])
        ax.text(edge.a[0],edge.a[1],edge.a[2],str(n))
    plt.show()
def meshShow(mesh):
    #Displays a mesh.
    print "unimplemented."

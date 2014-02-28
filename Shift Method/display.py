import scipy as sp
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import Basics

def edgePlot(path,numbers=False):
    #Displays path, a series of edge objects.
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    plt.xlabel('X')
    plt.ylabel('Y')
    for n in range(len(path)):
        edge = path[n]
        ax.plot([edge.a[0],edge.b[0]],[edge.a[1],edge.b[1]],[edge.a[2],edge.b[2]])
        if numbers:
            ax.text(edge.a[0],edge.a[1],edge.a[2],str(n))
    plt.show()
def pointPlot(points):
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    plt.xlabel('X')
    plt.ylabel('Y')
    xs = [point[0] for point in path]
    ys = [point[1] for point in path]
    zs = [point[2] for point in path]
    ax.scatter(xs,ys,zs)
    plt.show()

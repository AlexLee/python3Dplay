import scipy as sp
import math

import Basics
import mesh

class surface:
    #Parent class which will contain the shift functions.
    def pointShift(self,p):
        #Returns point p shifted vertically by its functional value.
        return p+sp.array([0,0,self.f(p)])
    def edgeShift(self,e):
        #Returns edge e with its endpoints shifted vertically by their functional values. This does not interpolate at all, so large edges will have problems.
        return Basics.edge(self.pointShift(e.a),self.pointShift(e.b))
    def triShift(self,t):
        #Returns tri t with its vertices shifted vertically by their functional values.
        return Basics.tri([self.pointShift(t.points[0]),self.pointShift(t.points[1]),self.pointShift(t.points[2])])
    def meshShift(self,m):
        #Returns mesh m with triShift applied to all its triangles.
        newTris = []
        for tri in m.tris:
            newTris.append(self.triShift(tri))
        return mesh.mesh(newTris)
    def dDeriv(self,v,p):
        #Returns the directional derivative of f along v at p as a scalar.
        v[0][2]=0 #Flattening v if it wasn't already.
        uv = Basics.unit(v)[0]
        uv = sp.array([uv[0],uv[1]])        #Turning uv 2D so that the dot product works
        return sp.dot(self.grad(p),uv)
    def vectorWrap(self,v,d):
        #Wraps of vector of XY (Vector will be projected to XY if it isn't yet.) onto the surface by turning it into a series of vectors end to end such that no point on any of the vectors is more than delta (d) from its
        #functional value in Z. Delta is kept in check using tangent plane approximation, so for large deltas you may get actual errors very different from delta. Returns a list of vectors.
        output = []
        XYlength = sp.sqrt(v[0][0]**2+v[0][1]**2)
        traveled = 0
        pos = sp.array([v[1][0],v[1][1],self.f(v[1])])
        XY = sp.array([pos[0],pos[1],0])
        uv = Basics.unit(v)[0]
        uv[2]=0
        while traveled<XYlength:
            derivative = self.dDeriv(v,pos)    #Directional derivative
            if derivative==0:
                dXY = 5*d
            else:
                dXY = d/derivative     #Distance to move in XY
            newXY = XY + uv*dXY
            move = [newXY[0]-XY[0],newXY[1]-XY[1],self.f(newXY)-pos[2]]
            output.append(sp.array([move,pos]))
            XY = newXY
            pos = pos+move
            traveled+=sp.sqrt(sp.sum(move[0]**2+move[1]**2))
        lastPos = sp.array([v[0][0]+v[1][0],v[0][1]+v[1][1],0])
        lastPos += sp.array([0,0,self.f(lastPos)])
        output[-1]=sp.array([lastPos-output[-1][1],output[-1][1]])
        return output

class wave(surface):
    #A sin wave projected along X or Y of form f(x,y)=a*sin(offset+2*pi*axis/l). Axis is 0 for x and 1 for y.
    def __init__(self,a,l,offset,axis):
        self.a = a
        self.l = l
        self.offset = offset
        self.axis = axis
    def f(self,p):
        #Returns the functional value of p.
        return self.a*math.sin(2*math.pi*p[self.axis]/self.l+self.offset)
    def grad(self,p):
        #Returns the gradient of f at p
        return sp.array([self.offset+2*math.pi*self.a*math.cos(2*math.pi*p[self.axis]/self.l)/self.l,0])

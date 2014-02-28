import scipy as sp
import math

import Basics
import mesh

class surface:
    '''
    Parent class which will contain the shift functions.
    '''
    def pointShift(self,p,u=1):
        '''
        Returns point p shifted vertically by its functional value * u
        '''
        return p+sp.array([0,0,u*self.f(p)])
    def edgeShift(self,e,u=1):
        '''
        Returns edge e with its endpoints shifted vertically by their functional values*u. This does not interpolate at all, so large edges will have problems.
        '''
        return Basics.edge(self.pointShift(e.a,u),self.pointShift(e.b,u))
    def triShift(self,t,u=1):
        '''
        Returns tri t with its vertices shifted vertically by their functional values. No interpolation is performed by this function.
        '''
        return Basics.tri([self.pointShift(t.points[0],u),self.pointShift(t.points[1],u),self.pointShift(t.points[2],u)])
    def meshShift(self,m,u=1):
        '''
        Returns mesh m with triShift applied to all its triangles.
        '''
        newTris = []
        for tri in m.tris:
            newTris.append(self.triShift(tri,u))
        return mesh.mesh(newTris)
    def dDeriv(self,v,p):
        '''
        Returns the directional derivative of f along v at p as a scalar.
        '''
        v[0][2]=0 #Flattening v if it wasn't already.
        uv = Basics.unit(v)[0]
        uv = sp.array([uv[0],uv[1]])        #Turning uv 2D so that the dot product works
        return sp.dot(self.grad(p),uv)
    def edgeWrap(self,e,n,up=True):
        '''
        Similar to edgeShift, but with edge broken up into n segments of equal XY length to fit the function better.
        '''
        points = [e.a+m*e.dir[0]*e.length/n for m in range(n)] + [e.b]
        shiftPoints = [self.pointShift(p,up) for p in points]
        return [Basics.edge(shiftPoints[k],shiftPoints[k+1]) for k in range(n)]                          

class wave(surface):
    '''
    A sin wave projected along X or Y of form f(x,y)=a*sin(2*pi*(shift+axis/l). Axis is 0 for x and 1 for y.
    '''
    def __init__(self,a,l,shift,axis):
        self.a = a
        self.l = l
        self.shift = shift
        self.axis = axis
    def f(self,p):
        #Returns the functional value of p.
        return self.a*math.sin(2*math.pi/self.l*(p[self.axis]+self.shift))
    def grad(self,p):
        #Returns the gradient of f at p
        if self.axis==0:
            return sp.array([self.a*2*math.pi/self.l*math.cos(2*math.pi/self.l*(p[self.axis]+self.shift)),0])
        else:
            return sp.array([0,self.a*2*math.pi/self.l*math.cos(2*math.pi/self.l*(p[self.axis]+self.shift))])
    def secGrad(self,p):
        '''
        Returns [Fxx,Fyy] at point p
        '''
        if self.axis==0:
            return sp.array([-self.a*(2*math.pi/self.l)**2*math.sin(2*math.pi/self.l*(p[self.axis]+self.shift)),0])
        else:
            return sp.array([0,-self.a*(2*math.pi/self.l)**2*math.sin(2*math.pi/self.l*(p[self.axis]+self.shift))])

import sympy
import Basics
import stl_importer
import mesh
import scipy as sp
sympy.init_session()

def planeConvert(bp):
    #Converts a Basics.plane object, bp, to a sympy function representing that plane.
    x,y,z=sympy.symbols('x y z')
    nor = bp.normal
    pos = bp.origin
    return sympy.Eq(nor[0]*(x-pos[0]) + nor[1]*(y-pos[1]) + nor[2]*(z-pos[2]),0)
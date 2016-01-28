from math import sqrt
import math
import math
import numpy
# Determines whether two circles collide and, if applicable,
# the points at which their borders intersect.
# Based on an algorithm described by Paul Bourke:
# http://local.wasp.uwa.edu.au/~pbourke/geometry/2circle/
# Arguments:
#   P0 (complex): the centre point of the first circle
#   P1 (complex): the centre point of the second circle
#   r0 (numeric): radius of the first circle
#   r1 (numeric): radius of the second circle
# Returns:
#   False if the circles do not collide
#   True if one circle wholly contains another such that the borders
#       do not overlap, or overlap exactly (e.g. two identical circles)
#   An array of two complex numbers containing the intersection points
#       if the circle's borders intersect.


def tri4(x1, x2, x3, y1, y2, y3, d1, d2, d3):
# f. wlasna
# xi, yi - wsp. wezlow
# di odleglosc od punktow
    if d1==0: d1=0.01
    if d2==0: d2=0.01
    if d3==0: d3=0.01
    #Wyznaczenie wsp. punktu pomi?dzy wezlami w proporcji od promieni
    [x12,y12]=Wsp_pkt_srodkowego(x1,x2,y1,y2,d1,d2)
    [x13,y13]=Wsp_pkt_srodkowego(x1,x3,y1,y3,d1,d3)
    [x23,y23]=Wsp_pkt_srodkowego(x2,x3,y2,y3,d2,d3)

    if odl_pkt(x1,y1,x2,y2) < max([d1, d2]):
      [x12,y12]=Wsp_pkt_srodkowego(x1,x2,y1,y2,d1,d2,-1)

    if odl_pkt(x1,y1,x3,y3) < max([d1, d3]):
      [x13,y13]=Wsp_pkt_srodkowego(x1,x3,y1,y3,d1,d3,-1)

    if odl_pkt(x2, y2, x3, y3) < max([d2, d3]):
      [x23,y23]=Wsp_pkt_srodkowego(x2,x3,y2,y3,d2,d3,-1)

    xx = [x12, x13, x23]
    yy = [y12, y13, y23]

    y = numpy.median(yy)

    xx[yy.index(y)] *= 2
    yy[yy.index(y)] *= 2

    x= sum(xx) / 4
    y= sum(yy) / 4

    return {'result': [x,y], 'point1' : [x12,y12], 'point2': [x13,y13], 'point3': [x23, y23]}


def median(arr, val, max):
    arr.append(val)

    if len(arr) > max:
       arr.pop(0)

    l = list(arr)

    if len(arr) > 3:
        l.pop(l.index(min(l)))
        l.pop(l.index(min(l)))

    return sum(l) / len(l)

def Rne_prostej(xn1,xn2,yn1,yn2):

    x = numpy.array([xn1, xn2])
    y = numpy.array([yn1, yn2])
    A = numpy.vstack([x, numpy.ones(len(x))]).T
    [m, c] = numpy.linalg.lstsq(A, y)[0]

    return [m, c]

def Wsp_pkt_srodkowego(x1,x2,y1,y2,d1,d2,sign=1):
    #zwraca wsp. punktu pomiedzy wezlami w miejscu wyznaczonym przez promienie
    if d2==0:
        d2=0.01
        print "d2=0"
    prop=sign*(d1/(d2*1.0))

    #x=(x1+x2)/2
    #y=(y1+y2)/2
    if 1+prop == 0:
        return [0,0]

    x=(x1+(prop*x2))/(1+prop)
    y=(y1+(prop*y2))/(1+prop)
    #x = x1 + prop * (x2 - x1);
    #y = y1 + prop * (y2 - y1);
    return [x,y]

def Rne_prostej_normal(a1,a2,b1,b2):
    #wyznacza wsp. prostej
    print "nic"

def Wsp_pkt_przeciecia(a1,a2,b1,b2):
    #Wyznacza wsp. punktu przeciecia 2 prostych
    if a2==a1:
        a2=2
        a1=1
    x=(b1-b2)/(a2-a1)
    y=(a2*b1-a1*b2)/(a2-a1)
    #y=a1*x+b1

    return [x,y]


def tri(x1, x2, x3, y1, y2, y3, d1, d2, d3):

    Vb=((d2**2 - d1**2) - (x2**2 - x1**2) - (y2**2 - y1**2))/2
    Va=((d2**2 - d3**2) - (x2**2 - x3**2) - (y2**2 - y3**2))/2

    y=(Vb*(x3-x2)-Va*(x1-x2))/((y1-y2)*(x3-x2)-(y3-y2)*(x1-x2))

    if x3-x2 == 0:
        return False

    x=(Va-y*(y3-y2))/(x3-x2)



    return [x,y]

def odl_pkt(wspXn1,wspYn1,wspXn2,wspYn2):
    return sqrt( (wspXn1 - wspXn2)**2 + (wspYn1 - wspYn2)**2 )

def lineMagnitude (x1, y1, x2, y2):
    lineMagnitude = math.sqrt(math.pow((x2 - x1), 2)+ math.pow((y2 - y1), 2))
    return lineMagnitude

#Calc minimum distance from a point and a line segment (i.e. consecutive vertices in a polyline).
def DistancePointLine (px, py, x1, y1, x2, y2):
    #http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
    LineMag = lineMagnitude(x1, y1, x2, y2)

    if LineMag < 0.00000001:
        DistancePointLine = 9999
        return DistancePointLine

    u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
    u = u1 / (LineMag * LineMag)

    if (u < 0.00001) or (u > 1):
        #// closest point does not fall within the line segment, take the shorter distance
        #// to an endpoint
        ix = lineMagnitude(px, py, x1, y1)
        iy = lineMagnitude(px, py, x2, y2)
        if ix > iy:
            DistancePointLine = iy
        else:
            DistancePointLine = ix
    else:
        # Intersecting point is on the line, use the formula
        ix = x1 + u * (x2 - x1)
        iy = y1 + u * (y2 - y1)
        DistancePointLine = lineMagnitude(px, py, ix, iy)

    return DistancePointLine


def IntersectPoints(P0, P1, r0, r1):
    if type(P0) != complex or type(P1) != complex:
        raise TypeError("P0 and P1 must be complex types")
    # d = distance
    d = sqrt((P1.real - P0.real)**2 + (P1.imag - P0.imag)**2)
    # n**2 in Python means "n to the power of 2"
    # note: d = a + b
    wsp=[]
    if d > (r0 + r1):
        return False
    elif d < abs(r0 - r1):
        return True
    elif d == 0:
        return True
    else:
        a = (r0**2 - r1**2 + d**2) / (2 * d)
        b = d - a
        h = sqrt(r0**2 - a**2)
        P2 = P0 + a * (P1 - P0) / d

        i1x = float(P2.real + h * (P1.imag - P0.imag) / d)
        i1y = P2.imag - h * (P1.real - P0.real) / d
        i2x = P2.real - h * (P1.imag - P0.imag) / d
        i2y = P2.imag + h * (P1.real - P0.real) / d
        wsp.append(float(i1x))
        wsp.append(float(i1y))
        wsp.append(float(i2x))
        wsp.append(float(i2y))
        #i1 = complex(i1x, i1y)
        #i2 = complex(i2x, i2y)

        #return [i1, i2, wsp]
        return [i1x,i1y,i2x,i2y]

def CompToStr(c):
    return "(" + str(c.real) + ", " + str(c.imag) + ")"

def PairToStr(p):
    return CompToStr(p[0]) + " , " + CompToStr(p[1])

def Test():
    ip = IntersectPoints

    i = ip(complex(10,0), complex(19, 2), 5, 6)
    #s = ip(complex(0,0), complex(4, 0), 2, 2)

    #print "Intersection:", PairToStr(i)
    #print "Wholly inside:", ip(complex(19,4), complex(10, 0), 5, 6)

    #print "Single-point edge collision:", PairToStr(s)
    #print "No collision:", ip(complex(1,0), complex(4, 0), 2, 2)


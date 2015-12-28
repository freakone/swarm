from math import sqrt
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

global duzo

duzo=10000000000

def Rne_prostej(xn1,xn2,yn1,yn2):
    #zwraca wspolczynniki a i b na podstawie wspolrzednej 2 punktow
    #print "x1i2 ,y12", xn1, xn2, yn1, yn2
    if xn1==xn2:
        wsp_a=1/duzo
        print "dzielenie przez zero"
    else:
        wsp_a =(yn2-yn1)/(xn2-xn1)
    wsp_b= (yn1-wsp_a*xn1)
    print "r-nie prostej a ab", wsp_a, wsp_b
    return [wsp_a,wsp_b]

def Wsp_pkt_srodkowego(x1,x2,y1,y2,d1,d2):
    #zwraca wsp. punktu pomiedzy wezlami w miejscu wyznaczonym przez promienie
    if d2==0:
        d2=0.01
        print "d2=0"
    prop=(d1/(d2*1.0))

    #x=(x1+x2)/2
    #y=(y1+y2)/2
    x=(x1+(prop*x2))/(1+prop)
    y=(y1+(prop*y2))/(1+prop)
    #x = x1 + prop * (x2 - x1);
    #y = y1 + prop * (y2 - y1);
    print "pkty srodkowe, x= ",x , " y= ", y
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
    #R-nia prostej przez dane wezly
    [a12,b12]=Rne_prostej(x1,x2,y1,y2)
    [a13,b13]=Rne_prostej(x1,x3,y1,y3)
    [a23,b23]=Rne_prostej(x2,x3,y2,y3)

    #R-nania prostych prostopadlych do powyzszych przechodzace przez punkty srodkowe
    if a12==0:
        a12p=1/duzo
        b12p=b12
        print "a12 duuuzo"
    else:
        a12p=-1/a12
        b12p=x12/a12+y12
        #b12p=-(a12p*x12)+y12
    if a13==0:
        a13p=1/duzo
        b13p=b13
        print "a13 duuuzo"
    else:
        a13p=-1/a13
        b13p=x13/a13+y13
        #b13p=-(a13p*x13)+y13 # - zle
    if a23==0:
        a23p=1/duzo
        b23p=b23
        print "a23 duuuzo"
    else:
        a23p=-1/a23
        #b23p=-(a23p*x23)+y23
        b23p=x23/a23+y23

    #wsp przecieca 2 punktw(kazdy z kazdym)
    [xp12_23,yp12_23]=Wsp_pkt_przeciecia(a12p,a23p,b12p,b23p)
    [xp13_23,yp13_23]=Wsp_pkt_przeciecia(a13p,a23p,b13p,b23p)
    [xp12_13,yp12_13]=Wsp_pkt_przeciecia(a12p,a13p,b12p,b13p)

    #Wyliczdnie sredniej
    x=(xp12_23+xp13_23+xp12_13)/3
    y=(yp12_23+yp13_23+yp12_13)/3
    print "tri 4 =", x, y
    return [x,y]


# nastepne funkcje
# przeciecie prostej i okregu

def line_circle_intersec(a,b,p,q,r):
    #a - wsp. kierunkowy funkcji
    #b - przesuniecie funkci
    #p,q - wspolrzednie srodka okregu,
    #r-promien okregu

    A=a**2+1
    B=2*(a*b-a*q-p)
    C=q**2-r**2+p**2-2*b*q+b**2
    Delta=B**2-4*A*C
    if Delta <0:
        print "<0"
        return [-1]
    else:
        x1=-B+math.sqrt(Delta)
        x2=-B-math.sqrt(Delta)
        y1=a*x1+b
        y2=a*x2+b
        return [x1,y1,x2,y2]



def line_circle_intersec2(a,b,p,q,r):
    #a - wsp. kierunkowy funkcji
    #b - przesuniecie funkci
    #p,q - wspolrzednie srodka okregu,
    #r-promien okregu
    dzielnik=2*(a**2+1)
    przed_pierw=(-2*a*b+2*a*q+2*p)
    pod_pierw=((2*a*b-2*a*q-2*p)**2)-4*(a**2+1)*(b**2-2*b*q+p**2+q**2-r**2)

    if pod_pierw <0:
        print "pod pierw <0"
        return []
    if dzielnik == 0:
        print "dzielnik =0"
        return [-1]
    else:
        xp1=(przed_pierw+math.sqrt(pod_pierw))/dzielnik
        xp2=(przed_pierw-math.sqrt(pod_pierw))/dzielnik
        yp1=a*xp1+b
        yp2=a*xp2+b
        #return [x1,y1,x2,y2]
    return [xp1,yp1,xp2,yp2]



def tri5(x1, x2, x3, y1, y2, y3, d1, d2, d3):
# f. wlasna
# xi, yi - wsp. wezlow
# di odleglosc od punktow
    if d1==0: d1=0.01
    if d2==0: d2=0.01
    if d3==0: d3=0.01
    #Wyznaczenie wsp. punktu pomiedzy wezlami w proporcji od promieni
    [x12,y12]=Wsp_pkt_srodkowego(x1,x2,y1,y2,d1,d2)
    [x13,y13]=Wsp_pkt_srodkowego(x1,x3,y1,y3,d1,d3)
    [x23,y23]=Wsp_pkt_srodkowego(x2,x3,y2,y3,d2,d3)

    #R-nie prostej pomiedzy wezlami sasiadami
    [a13,b13]=Rne_prostej(x1,x3,y1,y3)

    if a13==0:
        a13p=1/duzo
        b13p=b13
        print "a13 duuuzo"
    else:
        a13p=-1/a13
        #b13p=-(a13p*x13)+y13
        b13p=x13/a13+y13
    #punty wspolne dla prostej oraz okregu

    [Px1,Py1,Px2,Py2]=line_circle_intersec2(a13p,b13p,x2,y2,d2)
    print Px1,Py1,Px2,Py2

    return [Px1,Py1]










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


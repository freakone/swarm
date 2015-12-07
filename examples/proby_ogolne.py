from threading import Timer,Thread,Event
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from intersec_okr import *





NodyX=[0,5,10,12,19,17.5,24,25]
NodyY=[0,5,0,6.5,4,11,13,18]

trasaX=[0,2,4,6,8,10,12,14,16,18,19,20,21,22,23,25,26]
trasaY=[1.5,2,2.5,2.5,2.5,3,3.5,4,5,6.5,8,10,11.5,13,15,16,17]


pktX=[13]
pktY=[4.1]


dokl=0.3 #dokladnosc kreslania polozenia
nr_i=0
#lista L jest uzupe?niana cyklicznie podczas marszu
L=[13.5,8,5,2.6,6,8.5,1000,1000]
#Node wzwg. ktorego bedziemy nawigowac wyszukujemy najblizszy

nrN=3 # odleglosc od noda najblizszego (sasiednie N. musza byc dalej)

print "Odleglosc od noda najblizszego", L[nrN]
print "Wspolrzedna noda najblizszego", NodyX[nrN], NodyY[nrN]

circleN=plt.Circle((NodyX[nrN],NodyY[nrN]),L[nrN],color='b',fill=False)
circle_pop=plt.Circle((NodyX[nrN-1],NodyY[nrN-1]),L[nrN-1],color='b',fill=False)
circle_nast=plt.Circle((NodyX[nrN+1],NodyY[nrN+1]),L[nrN+1],color='b',fill=False)

#ip = IntersectPoints
i=[]
##trzeba sprawdzic, czy odleglosc pomiedzy puntami jest mniejsza niz suma promieni

i = IntersectPoints(complex(NodyX[nrN-1],NodyY[nrN-1]), complex(NodyX[nrN+1],NodyY[nrN+1]), L[nrN-1], L[nrN+1])
#i = X1 Y1 X2 Y2 - wspolrzednie punktow przciecia okregow
if i==False:
    print "brak rozwiazanie"

print "I=", len(i)
print "I2=", i[0], i[1]
odl_N_i1=odl_pkt(NodyX[nrN],NodyY[nrN],i[0],i[1])
odl_N_i2=odl_pkt(NodyX[nrN],NodyY[nrN],i[2],i[3])
print "Odl1 i 2", odl_N_i1, odl_N_i2

#odl1=odl_pkt(NodyX[nrN],NodyY[nrN],i[0],i[1])
#odl2=odl_pkt(NodyX[nrN],NodyY[nrN],i[2],i[3])
#print "dsda", odl1, odl2

if (odl_N_i1-L[nrN]<dokl): nr_i=0
else: nr_i=2

print "Numer i=", nr_i

plt.plot(i[nr_i], i[nr_i+1],'ro')
lista_min=[]
ind_min=0
wart_min=100000
#Wyszukanie puntu o min odleglosci
for licz in range(0,len(trasaX)):
    print odl_pkt(trasaX[licz],trasaY[licz],i[nr_i], i[nr_i+1])
    #lista_min[licz]=odl_pkt(trasaX[licz],trasaY[licz],i[nr_i], i[nr_i+1])
    wart_akt=odl_pkt(trasaX[licz],trasaY[licz],i[nr_i], i[nr_i+1])
    if wart_akt<=wart_min:
        wart_min=wart_akt
        ind_min=licz
print "min index=", ind_min
#znalezc 2 najblizszy punkt w traj.
#if [ind_min]
# !!! do zrobienia
#znalezc 2 punkty trasy najblizej punktu aktualnego
#z 2 punktow najbizszych zbudowac prosta i wyznaczyc odleglosc
# okreslic po ktorej stronie prostej jest punkt
#jesli odl jest za duza dac informacje o kierunku korekty...


#plt.plot(i[2], i[3],'bo')
#plt.plot(i[0], i[1], 'yo')




fig = plt.gcf()
#print len(trasaX)
#print len(trasaY)
#x1 = range(len(y1))
#x2 = range(len(y2))
#prawe
#plt.plot((0,0),(10,0),(19,4),(24,13), 'ro')
#lewe
#plt.plot((5,5),(12,6),(17,11),(25,18), 'bo')
plt.plot(NodyX, NodyY,'go')
#plt.plot(pktX, pktY,'ro')
plt.plot(trasaX, trasaY)
fig.gca().add_artist(circleN)
fig.gca().add_artist(circle_pop)
fig.gca().add_artist(circle_nast)


#plt.plot(x2, y2,'bo')
plt.axis([-5, max(NodyX)+2, -5, max(NodyY)+2])

plt.show()


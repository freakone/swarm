import matplotlib.pyplot as plt
import matplotlib.animation as anim
from collections import deque
import random
import serial


MAX_X = 200     #width of graph
MAX_Y = 800     #height of graph

try:
    ser = serial.Serial("COM4", baudrate=115200, timeout=0.1)
except:
    exit("brak portu COM")

i=0

global maxdata
global ind_kol
global okno

maxdata=100
ind_kol = 0
okno=20
data_srednia =[]
data10 =[]

# horizontal line
line = deque([0.0]*MAX_X, maxlen=MAX_X)
line2 = deque([0.0]*MAX_X, maxlen=MAX_X)
line3 = deque([0.0]*MAX_X, maxlen=MAX_X)
x=deque([0.0]*MAX_X, maxlen=MAX_X)

def update(fn, l2d,l2d2,l2d3,x):
    global ind_kol
    global okno
    global maxdata
    osx=0
    wy=0
    try:
        ser.write("RATO 0 000000000002\r\n")
        data1 = ser.readline() #.rstrip() # read data from serial
    except:
        print "Error: unable to start"
        pass
    if data1 == "":
        print ("Koniec danych")
        data1="000000000"
        pass
    try:
        dy=int(data1[3:9])
        print data1, dy
    except ValueError:
        print "Bladne dane"
        return
    if data1[1]=='0':
        last_data = int(data1[3:9]) # ostatnia dana z odczytu
        data10.insert(ind_kol,last_data)  # dodaj do listy, w miejsce najstarszej danej
        ind_kol = ind_kol+1
        if ind_kol>(okno):
            ind_kol=0
        if len(data10)==(okno+1): del data10[okno]
    else:
        print "Bylo zero", data1[1]

    wy10=sum(data10)
    print "Index", ind_kol, data10, wy10

    srednia=(wy10)/okno #liczneie sredniej
    #srednia2=(sum(data10)-min(data10)-max(data10))/(okno-2)

    srednia2=ind_kol
    #dodane nowego punktu do deque

    line.append(dy)
    line2.append(srednia)
    line3.append(srednia2)
    osx=osx+1
    x.append(osx)
    # set the l2d to the new line coords
    # args are ([x-coords], [y-coords])
    maxdata=max(data10)+10
    l2d.set_data(range(-MAX_X/2, MAX_X/2), line,)
    l2d2.set_data(range(-MAX_X/2, MAX_X/2), line2,)
    l2d3.set_data(range(-MAX_X/2, MAX_X/2), line3,)
'''
    if srednia2>9:

        plt.plot([1,2,3,srednia,8])
        plt.plot([1,2,3,4], [1,4,srednia2*4,16], 'ro')
    #plt.plot([1,3,3,5], [2,4,4,5])
        plt.axis([-1, 100, -1, 200])
    else:
        print("dd")
        #plt.cla()
    #plt.ylabel('m')
    '''
fig = plt.figure()
# make the axes revolve around [0,0] at the center
# instead of the x-axis being 0 - +100, make it -50 - +50
# ditto for y-axis -512 - +512
a = plt.axes(xlim=(0,MAX_X/2), ylim=(-(10),MAX_Y))
plt.tick_params(axis='y', which='both', labelleft='on', labelright='on')
#plt.autoscale_view(True,True,True)
#plt.yaxis.tick_right()

# plot an empty line and keep a reference to the line2d instance
l1, = a.plot([], [])
l2, = a.plot([], [])
l3, = a.plot([], [])

a.set_autoscale_on(True)
ani = anim.FuncAnimation(fig, update, fargs=(l1,l2,l3,x), interval=50)
plt.show()
ser.close()

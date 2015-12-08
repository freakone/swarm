from threading import Timer,Thread,Event
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from intersec_okr import *
import threading


class Visualizer:
  def __init__(self):
    self.nodeX=[0,500,1000,1200,1900,1750,2400,2500]
    self.nodeY=[0,500,0,650,400,1100,1300,1800]
    self.rootX=[0,200,400,600,800,1000,1200,1400,1600,1800,1900,2000,2100,2200,2300,2500,2600]
    self.rootY=[150,200,250,250,250,300,350,400,500,650,800,1000,1150,1300,1500,1600,1700]
    self.init_plot()
    self.compute_position(False)



  def set_point(self, x, y):
    self.person.remove()
    self.person, = plt.plot(x, y, 'ro')
    plt.pause(0.0001) 
    plt.draw()

  def compute_position(self, nodes):
    L=[1350,'nan',500,100,600,850,1000,'nan']

    font_point = {'family': 'serif',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }

    font_node = {'family': 'serif',
        'color':  'green',
        'weight': 'normal',
        'size': 10,
        }

    for n in range(0, len(L)):
      plt.text(self.nodeX[n]-80, self.nodeY[n]+80, "{}".format(L[n]), fontdict=font_node)


    index = []
    values = []
    for n in range(0,3):
      m = min(L)
      if not type(m) is int:
        print("not enough valid reads")
        return
      i = L.index(m)
      index.append(i)
      values.append(m)
      L[i] = 'nan'      

    for n in range(0,3):
      print(self.nodeX[index[n]], self.nodeY[index[n]], values[n])
      circle = plt.Circle((self.nodeX[index[n]],self.nodeY[index[n]]),values[n],color='b',fill=False)
      fig = plt.gcf()
      fig.gca().add_artist(circle)
      plt.pause(0.0001) 

    i = IntersectPoints(complex(self.nodeX[index[1]],self.nodeY[index[1]]), 
                        complex(self.nodeX[index[2]],self.nodeY[index[2]]),
                        values[1], values[2])

    if not i:
      print "no intersectrion"
      return

    i1=odl_pkt(self.nodeX[index[0]],self.nodeX[index[0]],i[0],i[1])
    i2=odl_pkt(self.nodeX[index[0]],self.nodeX[index[0]],i[2],i[3])

    if i2 > i1:
      searched_x, searched_y = i[0:2]
    else:
      searched_x, searched_y = i[2:4]

    plt.plot(searched_x, searched_y,'ro')
    plt.pause(0.0001) 

    root_length = []
    for n in range(0,len(self.rootX)):
      root_length.append(odl_pkt(self.rootX[n], 
                                  self.rootY[n],
                                  searched_x,
                                  searched_y))

    closest_root_point1 = root_length.index(min(root_length))
    root_length[closest_root_point1] = "nan"
    closest_root_point2 = root_length.index(min(root_length))

    plt.plot(self.rootX[closest_root_point1], self.rootY[closest_root_point1],'co')
    plt.plot(self.rootX[closest_root_point2], self.rootY[closest_root_point2],'co')
    plt.pause(0.0001) 

    distance = DistancePointLine(searched_x, searched_y, 
                            self.rootX[closest_root_point1], 
                            self.rootY[closest_root_point1],
                            self.rootX[closest_root_point2], 
                            self.rootY[closest_root_point2])

   

    plt.text(searched_x-100, searched_y+100, "{:0.1f}".format(distance), fontdict=font_point, bbox={'facecolor':'white', 'alpha':0.8, 'pad':1})


  def init_plot(self):
    plt.ion()    

    plt.axis([-500, max(self.nodeX)+500, -500, max(self.nodeY)+500])
    plt.plot(self.nodeX, self.nodeY,'go')   
    plt.plot(self.rootX, self.rootY, "--")
    plt.plot(self.rootX, self.rootY, 'k.')
    self.person, = plt.plot([], [], 'ro')  

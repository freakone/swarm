from threading import Timer,Thread,Event
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from intersec_okr import *
import threading
import time


class Visualizer:
  def __init__(self):
    self.nodeX=[0,500,1000,1200,1900,1750,2400,2500]
    self.nodeY=[0,500,0,650,400,1100,1300,1800]
    self.rootX=[0,200,400,600,800,1000,1200,1400,1600,1800,1900,2000,2100,2200,2300,2500,2600]
    self.rootY=[150,200,250,250,250,300,350,400,500,650,800,1000,1150,1300,1500,1600,1700]
    self.items = []
    self.init_plot()

  def chart_update(self):
    plt.pause(0.0001)
    plt.draw()

  def clear_items(self):
    for t in self.items:
      t.remove()
    self.items = []

  def set_point(self, x, y):
    self.person.remove()
    self.person, = plt.plot(x, y, 'ro')
    plt.pause(0.0001)
    plt.draw()

  def increase_3min(self, tab):

    tab_temp = list(tab)
    for n in range(0,3):
      m = min(tab_temp)
      i = tab_temp.index(m)
      tab[i] += 10
      tab_temp[i] = "nan"

    return tab


  def node_action(self, nodes, test=False):

    if test:
        L=[450,400,600,1233,1555,6234,1000,'nan']
    else:
        L = []
        for n in nodes:
          if n.availible:
            L.append(n.filtered_history[-1])
          else:
            L.append('nan')

    while True:
      ret = self.compute_positions(L)
      if ret == -2:
        print("increasing values")
        L = self.increase_3min(L)
      else:
        return ret


  def compute_positions(self, tab):

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

    self.clear_items()
    L = list(tab)

    for n in range(0, len(L)):
      txt = plt.text(self.nodeX[n]-80, self.nodeY[n]+80, "{}".format(L[n]), fontdict=font_node)
      self.items.append(txt)

    index = []
    values = []
    for n in range(0,3):
      m = min(L)
      if not type(m) is int:
        print("not enough valid reads")
        self.chart_update()
        return
      i = L.index(m)
      index.append(i)
      values.append(m)
      L[i] = 'nan'

    for n in range(0,3):
      circle = plt.Circle((self.nodeX[index[n]],self.nodeY[index[n]]),values[n],color='b',fill=False)
      fig = plt.gcf()
      fig.gca().add_artist(circle)
      self.items.append(circle)

    i = IntersectPoints(complex(self.nodeX[index[1]],self.nodeY[index[1]]),
                        complex(self.nodeX[index[2]],self.nodeY[index[2]]),
                        values[1], values[2])

    if not i:
      print "no intersectrion"
      return -2

    i1=odl_pkt(self.nodeX[index[0]],self.nodeX[index[0]],i[0],i[1])
    i2=odl_pkt(self.nodeX[index[0]],self.nodeX[index[0]],i[2],i[3])

    if i2 > i1:
      direction = "left"
      searched_x, searched_y = i[0:2]
    else:
      direction = "right"
      searched_x, searched_y = i[2:4]

    plt.plot(searched_x, searched_y,'ro')

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


    distance = DistancePointLine(searched_x, searched_y,
                            self.rootX[closest_root_point1],
                            self.rootY[closest_root_point1],
                            self.rootX[closest_root_point2],
                            self.rootY[closest_root_point2])


    txt = plt.text(-400, 2100, "Odleglosc od trasy: {:0.1f}".format(distance), fontdict=font_point, bbox={'facecolor':'white', 'alpha':0.8, 'pad':1})
    self.items.append(txt)

    if distance > 50:
        txt = plt.text(-400, 1900, "Za daleko, kierunek: {}".format(direction), fontdict=font_point, bbox={'facecolor':'red', 'alpha':0.5, 'pad':1})
        self.items.append(txt)

    self.chart_update()

  def init_plot(self):
    plt.ion()

    plt.axis([-500, max(self.nodeX)+500, -500, max(self.nodeY)+500])
    plt.plot(self.nodeX, self.nodeY,'go')
    plt.plot(self.rootX, self.rootY, "--")
    plt.plot(self.rootX, self.rootY, 'k.')
    self.person, = plt.plot([], [], 'ro')
    self.chart_update()

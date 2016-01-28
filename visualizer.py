from threading import Timer,Thread,Event
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from intersec_okr import *
import threading
import time
from vibrate import Vibrator


class Visualizer:
  def __init__(self, nodes):
    self.trace_max = 50
    self.complx = []
    self.comply = []

    self.nodes = nodes

    self.rootX=[125, 2000, 5100, 8500, 12600, 16200, 19200, 23500, 25100, 25000]
    self.rootY=[270, 500, 670, 860, 880, 760, 405, 58, -320, -560]


    self.items = []
    self.init_plot()
    self.flag = False

    self.MEDIAN = 10
    self.current_x = []
    self.current_y = []
    self.v = Vibrator()

    self.median_x = []
    self.median_y = []



  def chart_update(self):
    pt, = plt.plot(self.complx, self.comply, "--")
    self.items.append(pt)
    plt.pause(0.0001)
    plt.draw()

  def clear_items(self):
    for t in self.items:
      t.remove()
    self.items = []

  def set_point(self, x, y):
    self.person.remove()
    self.person, = plt.plot(x, y, 'ro')
    #plt.pause(0.0001)
    plt.draw()

  def graph(self, formula, x_range):
    x = np.array(x_range)
    y = eval(formula)
    pt, = plt.plot(x, y)
    self.items.append(pt)

  def increase_3min(self, tab):
    tab_temp = list(tab)
    for n in range(0,4):
      m = min(tab_temp)
      i = tab_temp.index(m)
      tab[i] += 50
      tab_temp[i] = "nan"

    return tab

  def node_action(self, nodes, test=False):
    if test:
       # L=[123334, 121345,603330,123333,155335,1800,500,1830]
      #  L=[10377,10400,'nan',6806,4442,2729,633,1454]
        #L= [11454,9753,6854,3656,110,3726,9097,13810,16102]
      L = [4218,5041,1060,2198,5670,9332,14473,19432,21743]
    else:
        L = []
        for n in nodes:
          if n.availible and n.a_counter < 30 and len(n.filtered_history) > 0:
            L.append(n.filtered_history[-1])
          else:
            L.append('nan')

#    self.compute_positions(L, nodes)
    while True:
       ret = self.compute_positions(L, nodes)
       if ret == -2:
         print("increasing values")
         L = self.increase_3min(L)
       else:
         return ret

  def compute_positions(self, tab, nodes):

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
      txt = plt.text(nodes[n].posX-80, nodes[n].posY+80, "{}".format(L[n]), fontdict=font_node)
      self.items.append(txt)

    index = []
    values = []

    m = min(L)
    i = L.index(m)
    index.append(i)
    values.append(m)

    L[i] = "nan"

    m = min(L)
    i = L.index(m)
    index.append(i)
    values.append(m)



    for m in values:
      if not type(m) is int:
        print("not enough valid reads")
        self.chart_update()
        return

    for n in range(0,len(index)):
      circle = plt.Circle((nodes[index[n]].posX,nodes[index[n]].posY),values[n],color='b',fill=False)
      fig = plt.gcf()
      fig.gca().add_artist(circle)
      self.items.append(circle)

    i = IntersectPoints(complex(nodes[index[0]].posX,nodes[index[0]].posY),
                        complex(nodes[index[1]].posX,nodes[index[1]].posY),
                        values[0], values[1])

    if type(i) is bool:
      print "no intersectrion"
      return -2

    if len(self.current_x) > 0:
      i1=odl_pkt(sum(self.current_x) / len(self.current_x) ,sum(self.current_y) / len(self.current_y),i[0],i[1])
      i2=odl_pkt(sum(self.current_x) / len(self.current_x) ,sum(self.current_y) / len(self.current_y),i[2],i[3])


      if i2 > i1:
        direction = "left"
        searched_x, searched_y = i[0:2]
        pt, = plt.plot(i[0], i[1],'co')
        self.items.append(pt)
      else:
        direction = "right"
        searched_x, searched_y = i[2:4]
        pt, = plt.plot(i[2], i[3],'co')
        self.items.append(pt)
    else:
      searched_x, searched_y = i[0:2]

    searched_x = median(self.current_x, searched_x, self.MEDIAN)
    searched_y = median(self.current_y, searched_y, self.MEDIAN)

    self.median_x.append(searched_x)

    if len(self.median_x) > len(self.current_x):
      self.median_x.pop(0)

    plt.figure(2)
    plt.clf()
    plt.plot(range(0, len(self.current_x)), self.current_x,'-', color='red')
    plt.plot(range(0, len(self.median_x)), self.median_x,'-', color='blue')
    plt.figure(1)

    pt, = plt.plot(searched_x, searched_y,'ro')
    self.complx.append(searched_x)
    self.comply.append(searched_y)

    if len(self.complx) > self.trace_max:
      self.complx.pop(0)
    if len(self.comply) > self.trace_max:
      self.comply.pop(0)

    self.items.append(pt)


    root_length = []
    for n in range(0,len(self.rootX)):
      root_length.append(odl_pkt(self.rootX[n],
                                  self.rootY[n],
                                  searched_x,
                                  searched_y))

    closest_root_point1 = root_length.index(min(root_length))
    root_length[closest_root_point1] = "nan"
    closest_root_point2 = root_length.index(min(root_length))

    if closest_root_point2 - closest_root_point1 != 1:
      root_length[closest_root_point2] = "nan"
      closest_root_point2 = root_length.index(min(root_length))

    pt, = plt.plot(self.rootX[closest_root_point1], self.rootY[closest_root_point1],'yo')
    self.items.append(pt)
    pt, = plt.plot(self.rootX[closest_root_point2], self.rootY[closest_root_point2],'yo')
    self.items.append(pt)

    distance = DistancePointLine(searched_x, searched_y,
                            self.rootX[closest_root_point1],
                            self.rootY[closest_root_point1],
                            self.rootX[closest_root_point2],
                            self.rootY[closest_root_point2])

    sign = ((self.rootX[closest_root_point2] - self.rootX[closest_root_point1]) * (searched_y - self.rootY[closest_root_point1]) - (self.rootY[closest_root_point2] - self.rootY[closest_root_point1]) * (searched_x - self.rootX[closest_root_point1]))

    direction = "lewo" if sign > 0 else "prawo"

    txt = plt.text(0, -500, "Odleglosc od trasy: {:0.1f}".format(distance), fontdict=font_point, bbox={'facecolor':'white', 'alpha':0.8, 'pad':1})
    self.items.append(txt)

    if distance > 50:
        txt = plt.text(0, -900, "Za daleko, kierunek: {}".format(direction), fontdict=font_point, bbox={'facecolor':'red', 'alpha':0.5, 'pad':1})
        self.items.append(txt)

    self.chart_update()


  def init_plot(self):
    plt.ion()
    mng = plt.get_current_fig_manager()

    plt.axis([-2000, max(map(lambda x: x.posX, self.nodes))+2000, -2000, max(map(lambda x: x.posY, self.nodes))+2000])
    plt.plot(map(lambda x: x.posX, self.nodes), map(lambda x: x.posY, self.nodes),'go')
    self.person, = plt.plot([], [], 'ro')
    plt.plot(self.rootX, self.rootY, "--")
    plt.plot(self.rootX, self.rootY, 'k.')
    self.chart_update()



    plt.figure(2)
    a = plt.axes(xlim=(-300,300), ylim=(-1000,1000))
    plt.tick_params(axis='y', which='both', labelleft='on', labelright='on')
    plt.figure(1)

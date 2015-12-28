from threading import Timer,Thread,Event
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from intersec_okr import *
import threading
import time
from vibrate import Vibrator


class Visualizer:
  def __init__(self):
    # self.nodeX=[0, 2300, 4100, 6040]
    # self.nodeY=[0, 530, 0, 1190]
    # self.nodeX=[0, 2277, 2277+1144, 2277+1144+1960]
    # self.nodeY=[0, 630, 0, 630+565]
    self.complx = []
    self.comply = []

    self.nodeX = [0, 0, 1936, 3964, 5934, 7594, 9494, 11694]
    self.nodeY = [0, 250, 0, 250, 0, 250, 0, 220]

    # self.nodeX = [0, 0.,   3151.6,  6327.6, 10076.,  13652.8,  18924.6,  23740.7,  25985.]
    # self.nodeY = [0, 539., 897.6,   379.3,  1239.,    584.5,    985.,   -362.2,    -644.1  ]

    # self.nodeX = [0, 556, 556]
    # self.nodeY = [0, 0, 300]

    self.rootX=[0,200,400,600,800,1000,1200,1400,1600,1800,1900,2000,2100,2200,2300,2500,2600]
    self.rootY=[150,200,250,250,250,300,350,400,500,650,800,1000,1150,1300,1500,1600,1700]
    self.items = []
    self.init_plot()
    self.flag = False

    self.MEDIAN = 30
    self.current_x = []
    self.current_y = []
    self.v = Vibrator()

   

  def chart_update(self):
    plt.plot(self.complx, self.comply, "--")
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

    # self.compute_positions(L)
    multi = 1
    cnt = 0
    while True:
      ret = self.compute_positions(L, multi)
      
      if cnt >  10:
        return []
      elif ret == -2:
        print("increasing values")
        multi = multi + 0.1
        cnt = cnt + 1
      else:
        return ret

  def compute_positions(self, tab, multi=1):

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

    m = min(L)

    i = L.index(m)
    index.append(i)
    values.append(m)

    if i == 0:
      index.append(i+1)
      values.append(L[i+1])
      index.append(i+2)
      values.append(L[i+2])
    elif i == len(L)-1:
      index.append(i-1)
      values.append(L[i-1])
      index.append(i-2)
      values.append(L[i-2])
    else:
      index.append(i-1)
      values.append(L[i-1])
      index.append(i+1)
      values.append(L[i+1])

    for m in values:
      if not type(m) is int:
        print("not enough valid reads")
        self.chart_update()
        return

    for n in range(0,3):
      circle = plt.Circle((self.nodeX[index[n]],self.nodeY[index[n]]),values[n],color='b',fill=False)
      fig = plt.gcf()
      fig.gca().add_artist(circle)
      self.items.append(circle)

    ret = tri4(self.nodeX[index[1]], self.nodeX[index[0]], self.nodeX[index[2]],
              self.nodeY[index[1]], self.nodeY[index[0]], self.nodeY[index[2]],
                                values[1], values[0], values[2])
    

    [searched_x,searched_y] = ret

    searched_x = median(self.current_x, searched_x, self.MEDIAN)
    searched_y = median(self.current_y, searched_y, self.MEDIAN)

    pt, = plt.plot(searched_x, searched_y,'ro')
    self.complx.append(searched_x)
    self.comply.append(searched_y)
    self.items.append(pt)

    if i > len(self.nodeX) - 3:  
      distance = DistancePointLine(searched_x, searched_y,
                            self.nodeX[i],
                            self.nodeY[i],
                            self.nodeY[i-2],
                            self.nodeY[i-2])
    else:
      distance = DistancePointLine(searched_x, searched_y,
                            self.nodeX[i],
                            self.nodeY[i],
                            self.nodeY[i+2],
                            self.nodeY[i+2])


    txt = plt.text(0, max(self.nodeY)+1500, "Odleglosc od trasy: {:0.1f}".format(distance), fontdict=font_point, bbox={'facecolor':'white', 'alpha':0.8, 'pad':1})
    self.items.append(txt)

    if distance < 100:
        if i % 2 == 0:
          direction = "lewo"
          self.v.command('lewo')
        else:
          direction = "prawo"
          self.v.command('prawo')

        txt = plt.text(0, max(self.nodeY)+1000, "Za daleko, kierunek: {}".format(direction), fontdict=font_point, bbox={'facecolor':'red', 'alpha':0.5, 'pad':1})
        self.items.append(txt)
    else:
       self.v.command('stop')

    self.chart_update()

  def init_plot(self):
    plt.ion()
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.axis([-2000, max(self.nodeX)+2000, -2000, max(self.nodeY)+2000])
    plt.plot(self.nodeX, self.nodeY,'go')
    #plt.plot(self.rootX, self.rootY, "--")
    #plt.plot(self.rootX, self.rootY, 'k.')
    self.person, = plt.plot([], [], 'ro')
    self.chart_update()

from threading import Timer,Thread,Event
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from intersec_okr import *
import threading
import time
from vibrate import Vibrator
import socket
import json

class Visualizer:
  def __init__(self):
    self.trace_max = 50
    self.complx = []
    self.comply = []

    self.items = []
    self.nodes = []

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    self.sock.bind(("127.0.0.1", 5005))


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
    plt.draw()

  def graph(self, formula, x_range):
    x = np.array(x_range)
    y = eval(formula)
    pt, = plt.plot(x, y)
    self.items.append(pt)


  def loop(self, data):

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


    for n in range(0, len(self.nodes[0])):
      txt = plt.text(self.nodes[0][n]-80, self.nodes[1][n]+80, "{}".format(data["distances"][n]), fontdict=font_node)
      self.items.append(txt)

    for n in range(0,len(data["indexes"])):
      circle = plt.Circle((self.nodes[data["indexes"][n]][0],self.nodes[data["indexes"][n]][1]),data["indexes"][n],color='b',fill=False)
      fig = plt.gcf()
      fig.gca().add_artist(circle)
      self.items.append(circle)

    pt, = plt.plot(data["point"][0], data["point"][1],'co')
    self.items.append(pt)

    self.complx.append(data["point"][0])
    self.comply.append(data["point"][1])

    if len(self.complx) > self.trace_max:
      self.complx.pop(0)
    if len(self.comply) > self.trace_max:
      self.comply.pop(0)

    pt, = plt.plot(self.nodes[2][data["closest_root"][0]], self.nodes[3][data["closest_root"][0]],'yo')
    self.items.append(pt)
    pt, = plt.plot(self.nodes[2][data["closest_root"][1]], self.nodes[3][data["closest_root"][1]],'yo')
    self.items.append(pt)

    if data.has_key("distance"):

      txt = plt.text(0, -500, "Odleglosc od trasy: {:0.1f}".format(data["distance"]), fontdict=font_point, bbox={'facecolor':'white', 'alpha':0.8, 'pad':1})
      self.items.append(txt)

      if distance > 50:
          txt = plt.text(0, -900, "Za daleko, kierunek: {}".format(data["direction"]), fontdict=font_point, bbox={'facecolor':'red', 'alpha':0.5, 'pad':1})
          self.items.append(txt)

    self.chart_update()


  def init_plot(self, nodes):
    self.nodes = nodes
    plt.ion()
    mng = plt.get_current_fig_manager()
    plt.axis([-2000, max(nodes[0])+2000, -3000, max(nodes[1])+3000])
    plt.plot(nodes[0], nodes[1],'go')
    self.person, = plt.plot([], [], 'ro')
    plt.plot(nodes[2], nodes[3], "--")
    plt.plot(nodes[2], nodes[3], 'k.')
    self.chart_update()

v = Visualizer()
actions = {"init": v.init_plot, "loop": v.loop}

def socket_action():
  while True:
    data, add = v.sock.recvfrom(1024)
    js = json.loads(data)
    actions[js["info"]](js["data"])
    print data

thr = threading.Thread(target=socket_action)
thr.setDaemon(True)
thr.start()

while True:
  time.sleep(1)
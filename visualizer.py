from threading import Timer,Thread,Event
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from libs.intersec_okr import *
import threading
import time
from libs.vibrate import Vibrator
import socket
import json

class Visualizer:
  def __init__(self):
    self.TRACKER = ("127.0.0.1", 5005)
    self.trace_max = 50000
    self.complx = []
    self.comply = []

    self.items = []
    self.nodes = []
    self.state = "init"

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    self.sock.bind(("0.0.0.0", 5006))

  def init_chart_command(self):
    self.sock.sendto("init", self.TRACKER)

  def chart_update(self):
    font_point = {'family': 'serif',
        'color':  'blue',
        'weight': 'bold',
        'size': 10,
        }
    axes = plt.gca()
    y = axes.get_ylim()
    x = axes.get_xlim()
    txt = plt.text(x[0], y[1]+200, self.state, fontdict=font_point)
    self.items.append(txt)
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

    font_error = {'family': 'serif',
        'color':  'red',
        'weight': 'normal',
        'size': 20,
        }

    self.clear_items()

    axes = plt.gca()
    y = axes.get_ylim()
    x = axes.get_xlim()

    for n in range(0, len(self.nodes[0])):
      txt = plt.text(self.nodes[0][n]-80, self.nodes[1][n]+80, "{}".format(data["distances"][n]), fontdict=font_node)
      self.items.append(txt)

    for i in data["indexes"]:
      if type(data["distances"][i]) is int:
        circle = plt.Circle((self.nodes[0][i],self.nodes[1][i]),data["distances"][i],color='b',fill=False)
        fig = plt.gcf()
        fig.gca().add_artist(circle)
        self.items.append(circle)

    if "error" in data:
       txt = plt.text(0, int(min(y)) + 2000, data["error"], fontdict=font_error, bbox={'facecolor':'red', 'alpha':0.5, 'pad':1})
       self.items.append(txt)
       self.chart_update()
       return

    txt = plt.text(x[0] + 5000, y[1]+200, data["time"], fontdict=font_node)
    self.items.append(txt)

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

    if data.has_key("root_distance"):
      txt = plt.text(x[0] + 30000, y[1]+200, "Odleglosc od trasy: {:0.1f}".format(data["root_distance"]), fontdict=font_node)
      self.items.append(txt)
      # print data["root_distance"]

      # if distance > 50:
      #     txt = plt.text(0, -900, "Za daleko, kierunek: {}".format(data["direction"]), fontdict=font_point, bbox={'facecolor':'red', 'alpha':0.5, 'pad':1})
      #     self.items.append(txt)

    self.chart_update()

  def ping(self, data):
    self.state = "RPI state: {}".format(['off', 'on'][data])
    if not data:
      self.clear_items()
      self.chart_update()


  def init_plot(self, nodes):
    print nodes
    self.nodes = nodes
    plt.ion()
    plt.axis([-10000, max(nodes[0])+10000, -10000, max(nodes[1])+10000])
    plt.plot(nodes[0], nodes[1],'go')
    self.person, = plt.plot([], [], 'ro')
    plt.plot(nodes[2], nodes[3], "--")
    plt.plot(nodes[2], nodes[3], 'k.')
    self.chart_update()
    self.inited = True

v = Visualizer()
actions = {"init": v.init_plot, "loop": v.loop, "ping": v.ping}

def socket_action():
  while True:
    data, add = v.sock.recvfrom(1024)
    js = json.loads(data)
    actions[js["info"]](js["data"])

thr = threading.Thread(target=socket_action)
thr.setDaemon(True)
thr.start()

v.init_chart_command()

while True:
  time.sleep(1)
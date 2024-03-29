from threading import Timer,Thread,Event
import numpy as np
from intersec_okr import *
import threading
import time
import socket
import json


class Tracker:
  def __init__(self, nodes):
    self.trace_max = 50
    self.complx = []
    self.comply = []

    self.nodes = nodes

    self.rootX=[0, 1200, 2700, 5000, 10000, 15000, 20000, 25000, 30000]
    self.rootY=[3060, 3060, 3060, 3060, 3060, 3060, 3060, 3060, 3060]

    self.MEDIAN = 10
    self.current_x = []
    self.current_y = []

    self.x = np.matrix('0. 0. 0. 0.').T
    self.P = np.matrix(np.eye(4))*1000
    self.R = 0.01**2

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    self.sock.bind(("0.0.0.0", 5005))
    self.clients = []

    # self.send_json("init", [map(lambda x: x.posX, self.nodes), map(lambda x: x.posY, self.nodes), self.rootX, self.rootY], ("127.0.0.1", 5006))
    thr = threading.Thread(target=self.socket_action)
    thr.setDaemon(True)
    thr.start()

  def clear(self):
    self.current_x = []
    self.current_y = []

  def socket_action(self):
    while True:
      data, add = self.sock.recvfrom(1024)
      if data == "init":
        self.send_json("init", [map(lambda x: x.posX, self.nodes), map(lambda x: x.posY, self.nodes), self.rootX, self.rootY], add)
        if not add in self.clients:
          self.clients.append(add)
          print add

  def send_ping(self, state):
    self.send_json("ping", state)

  def send_json(self, what, data, addr=""):
    if addr == "":
      for c in self.clients:
        try:
          self.sock.sendto(json.dumps({"info": what, "data": data}), c)
        except:
          print "ex"
          self.clients.remove(c)
    else:
      self.sock.sendto(json.dumps({"info": what, "data": data}), addr)

  def node_action(self, nodes):
    L = []
    for n in nodes:
      if n.availible and n.a_counter < 30 and len(n.filtered_history) > 0:
        L.append(n.filtered_history[-1])
      else:
        L.append('nan')

    return self.compute_positions(L, nodes)

  def compute_positions(self, tab, nodes):

    json_send = {"distances": tab, "time": "aaa"} #nodes[0].current_time}

    L = list(tab)

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

    json_send["indexes"] = index

    for m in values:
      if not type(m) is int:
        json_send["error"] = "not enough valid reads"
        self.send_json("loop", json_send)
        return False

    index.sort()

    i = IntersectPoints(complex(nodes[index[1]].posX,nodes[index[1]].posY),
                        complex(nodes[index[0]].posX,nodes[index[0]].posY),
                        values[1], values[0])

    if type(i) is bool:
      json_send["error"] = "calc error"
      self.send_json("loop", json_send)
      return False

    if len(self.current_x) > 0:
      i1=odl_pkt(sum(self.current_x) / len(self.current_x) ,sum(self.current_y) / len(self.current_y),i[0],i[1])
      i2=odl_pkt(sum(self.current_x) / len(self.current_x) ,sum(self.current_y) / len(self.current_y),i[2],i[3])


      if i2 > i1:
        direction = "left"
        searched_x, searched_y = i[0:2]
      else:
        direction = "right"
        searched_x, searched_y = i[2:4]
    else:
      searched_x, searched_y = i[0:2]

    searched_x = median(self.current_x, searched_x, self.MEDIAN)
    searched_y = median(self.current_y, searched_y, self.MEDIAN)

    self.x, self.P = kalman_xy(self.x, self.P, [searched_x, searched_y], self.R)
    searched_x, searched_y = map(lambda m: m[0], self.x[:2].tolist())
    json_send["point"] = [searched_x, searched_y]

    root_length = []
    for n in range(0,len(self.rootX)):
      root_length.append(odl_pkt(self.rootX[n],
                                  self.rootY[n],
                                  searched_x,
                                  searched_y))

    closest_root_point1 = root_length.index(min(root_length))
    root_length[closest_root_point1] = "nan"
    closest_root_point2 = root_length.index(min(root_length))

    root = [closest_root_point1, closest_root_point2]
    root.sort()

    json_send["closest_root"] = root

    if root[1] - root[0] != 1:
      root_length[root[1]] = "nan"
      root[1] = root_length.index(min(root_length))

    distance = dist(searched_x, searched_y,
                          self.rootX[root[0]],
                          self.rootY[root[0]],
                          self.rootX[root[1]],
                          self.rootY[root[1]])

    sign = ((self.rootX[root[1]] - self.rootX[root[0]]) * (searched_y - self.rootY[root[0]]) - (self.rootY[root[1]] - self.rootY[root[0]]) * (searched_x - self.rootX[root[0]]))
    direction = "lewo" if sign > 0 else "prawo"

    json_send["root_distance"] = distance
    json_send["direction"] = direction

    self.send_json("loop", json_send)

    return {'dist': distance, 'dir': direction, 'pos': [searched_x, searched_y]}



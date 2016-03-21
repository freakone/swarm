from threading import Timer,Thread,Event
import numpy as np
from intersec_okr import *
import threading
import time
from vibrate import Vibrator
import socket
import json


class Tracker:
  def __init__(self, nodes):
    self.trace_max = 50
    self.complx = []
    self.comply = []

    self.nodes = nodes

    self.rootX=[0, 2500, 2700, 3000, 5000, 10000, 15000, 20000, 25000, 30000]
    self.rootY=[2300, 2300, 2300, 2300, 2300, 2300, 2500, 2500, 2500, 2500]

    self.MEDIAN = 10
    self.current_x = []
    self.current_y = []
    self.v = Vibrator()

    self.median_x = []
    self.median_y = []
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    self.IP = "127.0.0.1"
    self.PORT = 5005

    self.send_json("init", [map(lambda x: x.posX, nodes), map(lambda x: x.posY, nodes), self.rootX, self.rootY])


  def send_json(self, what, data):
    self.sock.sendto(json.dumps({"info": what, "data": data}), (self.IP, self.PORT))

  def increase_3min(self, tab):
    tab_temp = list(tab)
    for n in range(0,3):
      m = min(tab_temp)
      i = tab_temp.index(m)
      tab[i] += 60
      tab_temp[i] = "nan"

    return tab

  def node_action(self, nodes):
    L = []
    for n in nodes:
      if n.availible and n.a_counter < 30 and len(n.current_data) > 0:
        L.append(n.current_data[-1])
      else:
        L.append('nan')

    cnt = 0
    while True:
       ret = self.compute_positions(L, nodes)
       if ret == -2 and cnt < 10:
        # print("increasing values")
         L = self.increase_3min(L)
         cnt = cnt + 10
       else:
         return ret

  def compute_positions(self, tab, nodes):

    json_send = {"distances": tab}

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
        print("not enough valid reads")
        self.chart_update()
        return


# !!! w wywolaniu funkcji zamieniono kolejnosc wezlow (indeksy 1 na 0), aby wybrac wlasciwe rozwiazanie
    i = IntersectPoints(complex(nodes[index[1]].posX,nodes[index[1]].posY),
                        complex(nodes[index[0]].posX,nodes[index[0]].posY),
                        values[1], values[0])

    if type(i) is bool:
      return -2

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

    json_send["point"] = [searched_x, searched_y]

    self.median_x.append(searched_x)

    if len(self.median_x) > len(self.current_x):
      self.median_x.pop(0)

    root_length = []
    for n in range(0,len(self.rootX)):
      root_length.append(odl_pkt(self.rootX[n],
                                  self.rootY[n],
                                  searched_x,
                                  searched_y))

    closest_root_point1 = root_length.index(min(root_length))
    root_length[closest_root_point1] = "nan"
    closest_root_point2 = root_length.index(min(root_length))

    json_send["closest_root"] = [closest_root_point1, closest_root_point2]

    if closest_root_point2 - closest_root_point1 != 1:
      root_length[closest_root_point2] = "nan"
      closest_root_point2 = root_length.index(min(root_length))

      distance = DistancePointLine(searched_x, searched_y,
                            self.rootX[closest_root_point1],
                            self.rootY[closest_root_point1],
                            self.rootX[closest_root_point2],
                            self.rootY[closest_root_point2])

      sign = ((self.rootX[closest_root_point2] - self.rootX[closest_root_point1]) * (searched_y - self.rootY[closest_root_point1]) - (self.rootY[closest_root_point2] - self.rootY[closest_root_point1]) * (searched_x - self.rootX[closest_root_point1]))
      direction = "lewo" if sign > 0 else "prawo"

      json_send["root_distance"] = distance
      json_send["direction"] = direction

    self.send_json("loop", json_send)



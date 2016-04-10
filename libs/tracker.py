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

    self.MEDIAN = 8
    self.current_x = []
    self.current_y = []
    self.v = Vibrator()

    self.x = np.matrix('0. 0. 0. 0.').T
    self.P = np.matrix(np.eye(4))*1000
    self.R = 0.01**2

    self.median_x = []
    self.median_y = []
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    self.sock.bind(("0.0.0.0", 5005))
    self.clients = []

    thr = threading.Thread(target=self.socket_action)
    thr.setDaemon(True)
    thr.start()

  def socket_action(self):
    while True:
      data, add = self.sock.recvfrom(1024)
      print data
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

    self.compute_positions(L, nodes)

  def kalman_xy(self, x, P, measurement, R,
                motion = np.matrix('0. 0. 0. 0.').T,
                Q = np.matrix(np.eye(4))):
      """
      Parameters:
      x: initial state 4-tuple of location and velocity: (x0, x1, x0_dot, x1_dot)
      P: initial uncertainty convariance matrix
      measurement: observed position
      R: measurement noise
      motion: external motion added to state vector x
      Q: motion noise (same shape as P)
      """
      return self.kalman(x, P, measurement, R, motion, Q,
                    F = np.matrix('''
                        1. 0. 1. 0.;
                        0. 1. 0. 1.;
                        0. 0. 1. 0.;
                        0. 0. 0. 1.
                        '''),
                    H = np.matrix('''
                        1. 0. 0. 0.;
                        0. 1. 0. 0.'''))

  def kalman(self, x, P, measurement, R, motion, Q, F, H):
      '''
      Parameters:
      x: initial state
      P: initial uncertainty convariance matrix
      measurement: observed position (same shape as H*x)
      R: measurement noise (same shape as H)
      motion: external motion added to state vector x
      Q: motion noise (same shape as P)
      F: next state function: x_prime = F*x
      H: measurement function: position = H*x

      Return: the updated and predicted new values for (x, P)

      See also http://en.wikipedia.org/wiki/Kalman_filter

      This version of kalman can be applied to many different situations by
      appropriately defining F and H
      '''
      # UPDATE x, P based on measurement m
      # distance between measured and current position-belief
      y = np.matrix(measurement).T - H * x
      S = H * P * H.T + R  # residual convariance
      K = P * H.T * S.I    # Kalman gain
      x = x + K*y
      I = np.matrix(np.eye(F.shape[0])) # identity matrix
      P = (I - K*H)*P

      # PREDICT x, P based on motion
      x = F*x + motion
      P = F*P*F.T + Q

      return x, P

  def compute_positions(self, tab, nodes):

    json_send = {"distances": tab, "time": nodes[0].current_time}

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
        return


# !!! w wywolaniu funkcji zamieniono kolejnosc wezlow (indeksy 1 na 0), aby wybrac wlasciwe rozwiazanie
    i = IntersectPoints(complex(nodes[index[1]].posX,nodes[index[1]].posY),
                        complex(nodes[index[0]].posX,nodes[index[0]].posY),
                        values[1], values[0])

    if type(i) is bool:
      json_send["error"] = "calc error"
      self.send_json("loop", json_send)
      return

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

    self.x, self.P = self.kalman_xy(self.x, self.P, [searched_x, searched_y], self.R)
    json_send["point"] = map(lambda m: m[0], self.x[:2].tolist())

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



from libs.swarm_reader import SwarmReader
from libs.file_reader import FileReader
import time
import random
import threading
import sys
from enum import Enum
import RPi.GPIO as GPIO
import libs.rpi as rpi
from libs.tracker import Tracker


measurements = 0
returned = []

pi = rpi.RPI_HAL()

rd = SwarmReader()
rd.add_node(0x10, 0, 0)
rd.add_node(0x11, 500, 0)
rd.add_node(0x12, 20000, 0)
rd.log = True
rd.write_header()

t = Tracker(rd.NODES)

def ping():
  while True:
    t.send_ping(pi.state)
    time.sleep(1)

th = threading.Thread(target=ping)
th.setDaemon(True)
th.start()

while True:
  if pi.state == rpi.State.running:
    rd.update()
    ret = t.node_action(rd.NODES)
    if ret:
      returned.append(ret)
    time.sleep(0.05)
    measurements = measurements + 1

    if measurements > 40:
      print len(returned)
      if len(returned) > 20:
        print returned[-1]['dist']
        print returned[-1]['dir']

        if returned[-1]['dist'] > 150:
          if returned[-1]['dir'] == "prawo":
            pi.set_state(rpi.State.turn_right)
          else:
            pi.set_state(rpi.State.turn_left)
      else:
        pi.set_state(rpi.State.error)

      time.sleep(1.5)

      pi.set_state(rpi.State.stop)
      t.clear()
      rd.clear()
      returned = []
      measurements = 0
  else:
    time.sleep(0.1)
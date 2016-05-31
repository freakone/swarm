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
rd.add_node(0x11, 5000, 0)
rd.add_node(0x12, 10000, 0)
rd.add_node(0x13, 15000, 0)
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
    time.sleep(0.02)
    measurements = measurements + 1

    if measurements > 30:
      print len(returned)
      if len(returned) > 15:
        print returned[-1]['dist']
        print returned[-1]['dir']
        print returned[-1]['pos']

        if returned[-1]['dist'] > 100:
          if returned[-1]['dir'] == "prawo":
            pi.set_state(rpi.State.turn_right)
            time.sleep(1)
          else:
            pi.set_state(rpi.State.turn_left)
            time.sleep(1)
        else:
           pi.set_state(rpi.State.error)
           time.sleep(0.3)
      else:
        pi.set_state(rpi.State.error)
        time.sleep(1)

      pi.set_state(rpi.State.stop)
      t.clear()
      rd.clear()
      returned = []
      measurements = 0
  else:
    time.sleep(0.1)
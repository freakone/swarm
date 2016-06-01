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

def measure(forced):
  returned = []
  for i in range(0, 30):
    rd.update()
    ret = t.node_action(rd.NODES)
    if ret:
      returned.append(ret)
    time.sleep(0.02)

    if not pi.state == rpi.State.periodic and not forced:
      t.clear()
      rd.clear()
      return False

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
  return True


while True:
  if pi.state == rpi.State.periodic:
    if measure(False):
      for i in range(0,50):
        time.sleep(0.1)
        if not pi.state == rpi.State.periodic:
          break
  elif pi.state == rpi.State.running:
    print "on demand"
    measure(True)
    time.sleep(2)
  else:
    time.sleep(0.1)
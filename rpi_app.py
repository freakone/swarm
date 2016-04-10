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
rd.add_node(0x18, 14700, 150)
rd.add_node(0x15, 7500, 150)
rd.add_node(0x16, 2800, 100)
rd.add_node(0x10, 0, 0)
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
    t.node_action(rd.NODES)

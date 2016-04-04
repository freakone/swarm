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
rd.add_node(0x11, 0, 250)
rd.add_node(0x12, 0, 1936)
rd.add_node(0x13, 3964, 250)
rd.add_node(0x14, 5934, 0)
rd.add_node(0x15, 7594, 250)
rd.add_node(0x16, 9494, 0)
rd.add_node(0x17, 11694, 220)
rd.add_node(0x18, 13694, 220)
rd.add_node(0x19, 15694, 220)
rd.log = True
rd.write_header()

t = Tracker(rd.NODES)
while True:
  if pi.state == rpi.State.running:
    rd.update()
    t.node_action(rd.NODES)
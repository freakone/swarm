from reader import SwarmReader
from visualizer import Visualizer
from file_reader import FileReader
import time
import random
import threading
import Tkinter
import tkMessageBox

rd = SwarmReader()
rd.add_node(0x10, 0, 0)
rd.add_node(0x11, 0, 250)
rd.add_node(0x12, 0, 1936)
rd.add_node(0x13, 3964, 250)
rd.add_node(0x14, 5934, 0)
rd.add_node(0x15, 7594. 250)
rd.add_node(0x16, 9494, 0)
rd.add_node(0x17, 11694, 220)
rd.log = True

v = Visualizer()


while True:
  rd.update()
  v.node_action(rd.NODES)
  time.sleep(0.1)

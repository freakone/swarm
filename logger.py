from reader import SwarmReader
# from visualizer import Visualizer
from file_reader import FileReader
import time
import random
import threading
import Tkinter
import tkMessageBox
import sys

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

# v = Visualizer()

cnt = 0
while True:
  rd.update()
  sys.stdout.write("\r%d" % cnt)
  sys.stdout.flush()
  cnt = cnt + 1
  # v.node_action(rd.NODES)
  #time.sleep(0.001)

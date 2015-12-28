from reader import SwarmReader
from visualizer import Visualizer
from file_reader import FileReader
import time
import random
import threading
import Tkinter
import tkMessageBox

rd = SwarmReader()
rd.add_node(0x10)
rd.add_node(0x11)
rd.add_node(0x12)
rd.add_node(0x13)
rd.add_node(0x14)
rd.add_node(0x15)
rd.add_node(0x16)
rd.add_node(0x17)
rd.add_node(0x18)
rd.log = True

v = Visualizer()


while True:
  rd.update()
  v.node_action(rd.NODES)
  time.sleep(0.1)

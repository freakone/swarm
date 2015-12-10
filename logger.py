from reader import SwarmReader
from visualizer import Visualizer
import time
import random
import threading

# rd = SwarmReader()
# rd.add_node(1)
# rd.add_node(2)
# rd.add_node(4)
# rd.add_node(5)
# rd.add_node(6)
# rd.add_node(7)
# rd.add_node(8)
# rd.add_node(9)
# rd.log = True
v = Visualizer()

import Tkinter
import tkMessageBox

top = Tkinter.Tk()
def helloCallBack(event=None):
  print("next will be flagged")
  rd.flag = True

B = Tkinter.Button(top, text ="Flag entry", command = helloCallBack)
B.pack()
top.bind("<space>", helloCallBack)

v.node_action(False)
while True:
  #rd.update()
  #v.node_action(rd.NODES)
  time.sleep(0.1)

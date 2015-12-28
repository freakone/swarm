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

# v = Visualizer()

# top = Tkinter.Tk()
# def helloCallBack(event=None):
#   print("next will be flagged")
#   #rd.flag = True
#   v.flag = True
#
# B = Tkinter.Button(top, text ="Flag entry", command = helloCallBack)
# B.pack()
# top.bind("<space>", helloCallBack)

# fr = FileReader("proba2/normal2.txt")

while True:
  rd.update()
  #fr.read_next()
  #v.node_action(fr.NODES)
  #v.node_action(False, True)
  time.sleep(0.1)

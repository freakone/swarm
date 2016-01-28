from visualizer import Visualizer
from file_reader import FileReader
import time
import random
import threading


fr = FileReader("./szklarska testy/normal_4_srodkiem w dol_z zatrzymaniem.txt")
v = Visualizer(fr.NODES)

#v.node_action(False, True)

while True:
  fr.read_next()
  v.node_action(fr.NODES)
  #time.sleep(0.1)

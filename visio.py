from visualizer import Visualizer
from file_reader import FileReader
import time
import random
import threading


#fr = FileReader("./szklarska testy/normal_3_srodkiem do gory.txt")
fr = FileReader("./proba2/normal3.txt")
v = Visualizer(fr.NODES)

#v.node_action(False, True)

while True:
  fr.read_next()
  v.node_action(fr.NODES)
  #time.sleep(0.1)

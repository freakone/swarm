from visualizer import Visualizer
from file_reader import FileReader
import time
import random
import threading


#fr = FileReader("./szklarska testy/normal_3_srodkiem do gory.txt")
fr = FileReader("./szklarska testy 2/normal-brami do gory-zatrzymanie na 5s pomiedzy i podejscie na 5s do lewego noda.txt")
v = Visualizer(fr.NODES)

#v.node_action(False, True)

while True:
  fr.read_next()
  v.node_action(fr.NODES)
  #time.sleep(0.1)

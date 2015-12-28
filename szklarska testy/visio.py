from visualizer import Visualizer
from file_reader import FileReader
import time
import random
import threading

v = Visualizer()
fr = FileReader("dane_testowe.txt")

while True:
  fr.read_next()
  v.node_action(fr.NODES)
  time.sleep(0.1)
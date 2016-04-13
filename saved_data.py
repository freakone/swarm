from libs.file_reader import FileReader
from libs.tracker import Tracker
import time
import random
import threading

fr = FileReader("./data/testy_wroclaw_park/normal_50m_prosto_wolno.txt")
t = Tracker(fr.NODES)

while True:
  fr.read_next()
  t.node_action(fr.NODES)
  time.sleep(0.1)

from libs.file_reader import FileReader
from libs.tracker import Tracker
import time
import random
import threading



#fr = FileReader("./boisko testy 16.03.12/normal_25m_wolno_po_prosrej_V_ok 1_krok_na1s_od10_.txt")
fr = FileReader("./data/boisko testy 16.03.12/normal_50m_prosto_wolno.txt")
# fr = FileReader("./boisko testy 16.03.12/normal_100m_prosto_wolno.txt")
#fr = FileReader("./wroclaw_stadion1/2_po_kwadracie_normal.txt")
t = Tracker(fr.NODES)

while True:
  fr.read_next()
  t.node_action(fr.NODES)
  time.sleep(0.1)

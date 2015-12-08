from reader import SwarmReader
from visualizer import Visualizer
import time
import random

rd = SwarmReader()
rd.add_node(1)
rd.add_node(2)
rd.add_node(4)
rd.add_node(5)
rd.add_node(6)
rd.add_node(7)
rd.add_node(8)
rd.add_node(9)

v = Visualizer()

while True:
    rd.update()
    v.node_action(rd.NODES)
    v.updater()
    time.sleep(0.1)
    

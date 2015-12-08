from reader import SwarmReader
from visualizer import Visualizer
import time
import random

rd = SwarmReader()
rd.add_node(10)

v = Visualizer()

while True:
    #rd.update()
    v.set_point(random.random()*1000, random.random()*1000)
    time.sleep(0.1)

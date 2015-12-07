from reader import SwarmReader
import time

rd = SwarmReader()

while True:
    rd.update()
    time.sleep(0.2)

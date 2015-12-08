import serial
import serial.tools.list_ports
import time
from node import Node

class SwarmReader:
    def __init__(self):
        self.NODES = []
        self.COMPORT = "" 

        for c in serial.tools.list_ports.comports():
            if "FTDI" in c[2]:
                COMPORT = c[0]

        if COMPORT == "":
            exit("! no device connected")

        try:
            self.com = serial.Serial(COMPORT, baudrate=115200, timeout=0.1)
        except Exception as e:
            exit(e)

    def add_node(self, id):
        self.NODES.append(Node(id))

    def probe(self):
        for n in self.NODES:
            n.probe()

    def update(self):
        for n in self.NODES:
            try:
                self.com.write("RATO 0 {:012X}\r\n".format(n.id))
                line = self.com.readline()                
            except Exception as e:
                print(e)
                print("# com read error")
                continue

            n.availible = line[1] == '0'

            if not line[1] == '0':
                continue

            try:
                distance = int(line[3:9])               
                n.add_data(distance)
                print(line)
            except Exception as e:
                print(e)
                print("# data conversion error")
                continue

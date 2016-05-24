import serial
import serial.tools.list_ports
import time
import datetime
from node import Node

class SwarmReader:
    def __init__(self):
        self.NODES = []
        self.COMPORT = ""
        self.log = False
        self.f_norm = open('normal.txt', 'w')
        self.flag = False

        for c in serial.tools.list_ports.comports():
            if filter( lambda x: x in c[2], ["FTDI", "0403:6001"]):
                self.COMPORT = c[0]

        if self.COMPORT == "":
            exit("! no device connected")

        try:
            self.com = serial.Serial(self.COMPORT, baudrate=115200, timeout=0.1)
        except Exception as e:
            exit(e)

    def add_node(self, id, x, y):
        n = Node(id, x, y)
        n.set_pos(x, y)
        self.NODES.append(n)

    def probe(self):
        for n in self.NODES:
            n.probe()

    def write_header(self):
        for n in self.NODES:
            self.f_norm.write("%d;" % n.posX)
        self.f_norm.write("\n")
        for n in self.NODES:
            self.f_norm.write("%d;" % n.posY)
        self.f_norm.write("\n")

    def clear(self):
      for n in self.NODES:
        n.clear()

    def update(self):
        for n in self.NODES:
            try:
                command = "RATO 0 {:012X}\r\n".format(n.id)
                #print(command)
                self.com.write(command)
                line = "l"
                while line[0] != '=':
                    line = self.com.readline()
            except Exception as e:
                print(e)
                print("# com read error")
                continue

            n.availibility(line[1] == '0')

            if not line[1] == '0':
                if self.log:
                    self.f_norm.write("nan;")
                continue

            try:
                distance = line[3:9]
                if distance.find(".") > -1:
                    distance = int(100*float(distance))
                else:
                    distance = int(distance)

                filtered = n.add_data(distance)
                n.current_time = datetime.datetime.now();

                if self.log:
                    self.f_norm.write("%d;" % distance)
            except Exception as e:
                print(e)
                print("# data conversion error")
                continue
        if self.log:
            if self.flag:
                self.f_norm.write("flagged;")
                self.flag = False
                print("entry flagged")

            self.f_norm.write("%s" % datetime.datetime.now())

            self.f_norm.write("\n")

import time
from node import Node

class FileReader:
    def __init__(self, file):
        self.NODES = []
        self.f = open(file, 'r')

        linex = self.f.readline().split(";")
        liney = self.f.readline().split(";")
        for i in range(0, len(linex)-1):
            n = Node(i, float(linex[i]), float(liney[i]))
            n.availible = True
            self.NODES.append(n)

    def read_next(self):
        line = self.f.readline().split(";")

        time = line[-1].strip()

        for i in range(0, len(line)-1):
            if line[i] == "nan":
                self.NODES[i].a_counter += 1
            else:
                self.NODES[i].add_data(int(line[i]))

            self.NODES[i].current_time = time
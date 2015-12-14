import time
from node import Node

class FileReader:
    def __init__(self, file):
        self.NODES = []
        self.f = open(file, 'r')

    def read_next(self):
        line = self.f.readline().split(";")

        if len(self.NODES) == 0:
            for i in range(0, len(line)-1):
                n = Node(i)
                n.availible = True
                self.NODES.append(n)


        for i in range(0, len(line)-1):
            if line[i] == "nan":
                self.NODES[i].add_data(-1)
            else:
                self.NODES[i].add_data(int(line[i]))

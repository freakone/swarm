import serial
import serial.tools.list_ports
import time

class SwarmReader:
    def __init__(self):
        self.NODES = [{'id': 1, 'current_data' : [], 'filtered_history': [], 'selected': []},
                {'id': 2, 'current_data' : [], 'filtered_history': [], 'selected': []}]

        self.COMPORT = ""
        self.MAX_CURRENT = 20
        self.MAX_FILTERED = 500


        for c in serial.tools.list_ports.comports():
            if "FTDI" in c[2]:
                COMPORT = c[0]

        if COMPORT == "":
            exit("! no device connected")

        try:
            self.com = serial.Serial(COMPORT, baudrate=115200, timeout=0.1)
        except Exception as e:
            exit(e)

    def probe(self):
        for n in self.NODES:
            n['selected'].insert(n['filtered_history'][-1])


    def update(self):
        for n in self.NODES:
            try:
                self.com.write("RATO 0 {:012X}\r\n".format(n['id']))
                line = self.com.readline()
            except Exception as e:
                print(e)
                print("# com read error")
                continue

            if not line[1] == '0':
                continue

            try:
                distance = int(line[3:9])
                n['current_data'].append(distance)
                if len(n['current_data']) > self.MAX_CURRENT:
                    n['current_data'].pop(0)

                filtered = sum(n['current_data']) / len(n['current_data'])
                n['filtered_history'].append(filtered)
                if len(n['filtered_history']) > self.MAX_FILTERED:
                    n['filtered_history'].pop(0)

                print(line,distance,filtered)
            except Exception as e:
                print(e)
                print("# data conversion error")
                continue

import serial
# import serial.tools.list_ports
import time
from node import Node

class Vibrator:
    def __init__(self):
        self.COMPORT = ""
        # self.COMMANDS = {'lewo':":L", 'prawo':":P", 'stop':":S", 'live':":W"}

        # return

        # for c in serial.tools.list_ports.comports():
        #     if "1A86:7523" in c[2]:
        #         self.COMPORT = c[0]

        # if self.COMPORT == "":
        #     exit("! no device connected")

        # try:
        #     self.com = serial.Serial(self.COMPORT, baudrate=57600, timeout=0.1)
        # except Exception as e:
        #     exit(e)


    def command(self, cmd):
        try:
            self.com.write(self.COMMANDS[cmd])
        except Exception as e:
            print(e)
            print("# com write error")

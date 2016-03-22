import time
import random
import threading
import sys
from enum import Enum
import RPi.GPIO as GPIO


class State(Enum):
  running = 1
  stop = 0

class RPI_HAL:
  def __init__(self):
    GPIO.setup(20, GPIO.IN, pull_up_down=RPIO.PUD_UP)
    GPIO.setup(21, GPIO.IN, pull_up_down=RPIO.PUD_UP)
    GPIO.setup(2, GPIO.OUT)
    GPIO.setup(3, GPIO.OUT)
    self.state = State.stop


    th_led = threading.Thread(target=self.blinker)
    th.setDaemon(True)
    th.start()

  def blinker(self):
    if self.state == State.running:
      GPIO.output(2, !GPIO.input(2))
    else:
      GPIO.output(3, !GPIO.input(3))

    time.sleep(1)

  def set_state(self, state):
    self.state = state;
    GPIO.output(2, 0)
    GPIO.output(3, 0)
import time
import random
import threading
import sys
from enum import Enum
import RPi.GPIO as GPIO


GREEN = 17
RED = 27
BTN_START = 5
BTN_STOP = 6

class State(Enum):
  running = 1
  stop = 0

class RPI_HAL:
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BTN_STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BTN_START, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BTN_START, GPIO.FALLING, callback=self.button_callback)
    GPIO.add_event_detect(BTN_STOP, GPIO.FALLING, callback=self.button_callback)
    GPIO.setup(GREEN, GPIO.OUT)
    GPIO.setup(RED, GPIO.OUT)
    GPIO.output(GREEN, 1)
    GPIO.output(RED, 1)
    self.state = State.stop
    self.btntimes = {BTN_STOP: 1, BTN_START: 1}


    th_led = threading.Thread(target=self.blinker)
    th_led.setDaemon(True)
    th_led.start()

  def button_callback(self, channel):

    if time.clock() - self.btntimes[channel] < 0.5:
      return

    self.btntimes[channel] = time.clock()

    print time.clock()
    if channel == BTN_START:
      self.set_state(State.running)
    elif channel == BTN_STOP:
      self.set_state(State.stop)

  def blinker(self):
    while True:
      if self.state == State.running:
        GPIO.output(GREEN, not GPIO.input(GREEN))
      else:
        GPIO.output(RED, not GPIO.input(RED))
      time.sleep(1)

  def set_state(self, state):
    self.state = state;
    GPIO.output(GREEN, 1)
    GPIO.output(RED, 1)
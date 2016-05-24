import time
import random
import threading
import sys
from enum import Enum
import RPi.GPIO as GPIO


MOTOR = 17
BTN_START = 22
BTN_STOP = 27

class State(Enum):
  error = 4
  turn_left = 3
  turn_right = 2
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
    GPIO.setup(MOTOR, GPIO.OUT)
    GPIO.output(MOTOR, 0)
    self.state = State.stop
    self.btntimes = {BTN_STOP: 1, BTN_START: 1}
    self.alternate = False
    th_led = threading.Thread(target=self.blinker)
    th_led.setDaemon(True)
    th_led.start()

  def button_callback(self, channel):
    if time.time() - self.btntimes[channel] < 0.5:
      return

    self.btntimes[channel] = time.time()

    print time.time()
    if channel == BTN_START:
      self.set_state(State.running)
    elif channel == BTN_STOP:
      self.set_state(State.stop)

  def blinker(self):
    while True:
      if self.state == State.error:
        GPIO.output(MOTOR, 1)
      elif self.state == State.turn_right:
        GPIO.output(MOTOR, self.alternate)
        self.alternate = not self.alternate
        time.sleep(0.1)
      elif self.state == State.turn_left:
        GPIO.output(MOTOR, self.alternate)
        self.alternate = not self.alternate
      else:
        GPIO.output(MOTOR, 0)
      time.sleep(0.22)

  def set_state(self, state):
    self.state = state;
    GPIO.output(MOTOR, 0)
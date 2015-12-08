from threading import Timer,Thread,Event
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from intersec_okr import *
import threading


class Visualizer:
  def __init__(self):
    self.nodeX=[0,5,10,12,19,17.5,24,25]
    self.nodeY=[0,5,0,6.5,4,11,13,18]
    self.rootX=[0,2,4,6,8,10,12,14,16,18,19,20,21,22,23,25,26]
    self.rootY=[1.5,2,2.5,2.5,2.5,3,3.5,4,5,6.5,8,10,11.5,13,15,16,17]
    self.init_plot()


  def set_point(self, x, y):
    self.person.remove()
    self.person, = plt.plot(x, y, 'ro')
    plt.pause(0.0001) 
    plt.draw()

  def init_plot(self):
    plt.ion()    

    plt.axis([-5, max(self.nodeX)+5, -5, max(self.nodeY)+5])
    plt.pause(0.0001) 
    plt.plot(self.nodeX, self.nodeY,'go')   
    plt.pause(0.0001)  
    plt.plot(self.rootX, self.rootY, "--")
    plt.pause(0.0001) 
    plt.plot(self.rootX, self.rootY, 'k.')
    plt.pause(0.0001) 
    self.person, = plt.plot([], [], 'ro')
    plt.pause(0.0001) 

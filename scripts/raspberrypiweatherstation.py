#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
 
import os
from daemon import Daemon
#! /usr/bin/env python 

from gps import *
import RPi.GPIO as GPIO

import time
import threading
import yaml
import csv
import rrdtool


gpsd = None #seting the global variable
GPIO.setmode(GPIO.BCM) 
  

# handle the button event
def buttonEventHandler (pin):
    print "handling button event"

    # turn the green LED on
    GPIO.output(25,True)

    time.sleep(1)

    # turn the green LED off
    GPIO.output(25,False)


class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
 
# Logger # CSV

with open('test.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    data = [['Me', 'You'],
            ['293', '219'],
            ['54', '13']]
    a.writerows(data)
    fp.close()


# RRD 
from rrdtool import update as rrd_update
ret = rrd_update('example.rrd', 'N:%s:%s' %(metric1, metric2));

# Main Loop
if __name__ == '__main__':

  # tell the GPIO module that we want to use 
  # the chip's pin numbering scheme
  with open('config.yaml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
  
  for section in cfg:
    print(section)
  
  #GPS
  gpsp = GpsPoller() # create the thread

  # # setup pin 23 as an input
  # and set up pins 24 and 25 as outputs
  GPIO.setup(23,GPIO.IN)
  GPIO.setup(24,GPIO.OUT)
  GPIO.setup(25,GPIO.OUT)
  
  # tell the GPIO library to look out for an 
  # event on pin 23 and deal with it by calling 
  # the buttonEventHandler function
  GPIO.add_event_detect(23,GPIO.FALLING)
  GPIO.add_event_callback(23,buttonEventHandler)
  
  # turn off both LEDs
  GPIO.output(25,False)
  GPIO.output(24,True)



  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc

      print 'GPS reading'
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print 'altitude (m)' , gpsd.fix.altitude


      


      time.sleep(5) #set to whatever

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    #gpsp.join() # wait for the thread to finish what it's doing
  print "Almost done."
  GPIO.cleanup()
  print "Done.\nExiting."
  exit();


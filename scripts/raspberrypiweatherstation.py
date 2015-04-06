#! /usr/bin/python
# Based off the code written by Dan Mandle http://dan.mandle.me September 2012
# Modified by Kevin Kingsbury: https://github.com/kmkingsbury
# License: GPL 2.0
 
import os
from daemon import Daemon

from gps import *
import RPi.GPIO as GPIO

from time import gmtime, strftime
import threading
import yaml
import csv
import rrdtool

#Sesnsor libraries
from bmp183 import bmp183
#import Adafruit_DHT


gpsd = None #seting the global variable
#GPIO.setmode(GPIO.BCM) 
sensor = 11
DHpin = 7
SPICLK = 11 #17
SPIMISO = 18 #24
SPIMOSI = 22 #25
SPICS = 13 #27

humidity_adc = 0

mybutton = 40

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# handle the button event 
def buttonEventHandler (pin):
    print "handling button event"

    # turn the green LED on
    # GPIO.output(25,True)

    os.system("shutdown -h now")
    #time.sleep(1)

    # turn the green LED off
    #GPIO.output(25,False)

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
 
 


# RRD 
#from rrdtool import update as rrd_update
#ret = rrd_update('example.rrd', 'N:%s:%s' %(metric1, metric2));

# Main Loop
if __name__ == '__main__':

# Open Config file, use vars from that.
  with open('config.yaml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
  
  for section in cfg:
    print(section)


# Logger open CSV
  fp = open('test.csv', 'a')
  csv = csv.writer(fp, delimiter=',')


  
  #GPS
  gpsp = GpsPoller() # create the thread

  #Get Pressure and Temp Ready
  bmp = bmp183()


  # set up the SPI interface pins
  GPIO.setup(SPIMOSI, GPIO.OUT)
  GPIO.setup(SPIMISO, GPIO.IN)
  GPIO.setup(SPICLK, GPIO.OUT)
  GPIO.setup(SPICS, GPIO.OUT)


  GPIO.setup(mybutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  # # setup pin 23 as an input
  # and set up pins 24 and 25 as outputs
  # GPIO.setup(23,GPIO.IN)
  # GPIO.setup(24,GPIO.OUT)
  # GPIO.setup(25,GPIO.OUT)
  
  # tell the GPIO library to look out for an 
  # event on pin 23 and deal with it by calling 
  # the buttonEventHandler function
  GPIO.add_event_detect(mybutton,GPIO.FALLING)
  GPIO.add_event_callback(mybutton,buttonEventHandler)
  
  # turn off both LEDs
  # GPIO.output(25,False)
  # GPIO.output(24,True)
 
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data


      print 'GPS reading'
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print 'altitude (m)' , gpsd.fix.altitude

      timenow = str(gpsd.utc)+' + '+ str(gpsd.fix.time)
      if timenow is None or timenow == " + nan":
          #get now
          timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())


      #Pull Temp, Humidity, Pressure
      bmp.measure_pressure()
      print "Temperature: ", bmp.temperature, "deg C"
      print "Pressure: ", bmp.pressure/100.0, " hPa"

      bmptemp = bmp.temperature * 9/5 + 32
      bmppressure = bmp.pressure/100.0 #hPa

      #Pull Humidity & Temp
#      humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHpin, 10, .01)
#      if humidity is not None and temperature is not None:
#        print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
#      else:
#         humidity = "Nan"
#         temperature = "Nan"

      value = readadc(humidity_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
      supplyVolt = 5.09
      voltage = value/1024. * supplyVolt #// convert to voltage value
      sensorRH = 161.0 * voltage / supplyVolt - 25.8
      trueRH = sensorRH / (1.0546 - 0.0026 *  bmp.temperature)


      print "Val "+ str(value) + "Perc" + str(value/1023.) + " TH:"+str(trueRH)

      # GEt Light:
      light = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
      print "Light:"+ str(light) 


      #Wind Dir:

      #Wind Speed

      #Record to CSV
      data = [ timenow, gpsd.fix.latitude, gpsd.fix.longitude, bmptemp, trueRH, bmppressure, light ]
      print "Data: ",
      print (data)
      csv.writerow(data)
         
      #Sleep
      time.sleep(1) #set to whatever

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    
    gpsp.running = False
    #gpsp.join() # wait for the thread to finish what it's doing
  print "Almost done."
  fp.close()
  GPIO.cleanup()
  print "Done.\nExiting."
  exit();


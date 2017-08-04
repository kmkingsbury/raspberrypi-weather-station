import os, sys
import RPi.GPIO as GPIO
import time
import datetime
import numpy
import logging.config
import csv
import yaml
import structlog
from pathlib import Path

try:
    import thread
except ImportError:
    import _thread as thread


# Our Log Stuff
import loggerhelper

# Modules
from daemon import Daemon
from bmp183 import bmp183
import Adafruit_DHT

class CSVWriter:

  def __init__(self, filename='test.csv', header=[]):
    newfile = False
    self._header = header
    outfile = Path(filename)
    if not outfile.is_file():
        #File doesn't exist, will be created, print header too
        newfile = True
    self.fn = open(filename, 'a')
    self._day= datetime.date.today().day
    print("Date:" + str(self._day))
    self.csv = csv.writer(self.fn, delimiter=',')
    print("Size"+ str(len(header)))
    if (newfile == True):
      #new file so print header
      self.csv.writerow(self._header)

  def writedata(self,dataobj):
    if (self._day != datetime.date.today().day):
      dt = datetime.date.today()
      filename = "data-"+dt.strftime("%Y-%m-%d") + ".csv"
      self.fn.close()
      self = CSVWriter(filename, self._header)
      self.csv.writerow(self._header)
    self.csv.writerow(dataobj)

  def __del__(self):
    self.fn.close()


class StationConfig:
  def __init__(self, file='config.yaml'):
    with open(file, 'r') as ymlfile:
      try:
        self.configs = yaml.load(ymlfile)
      except yaml.YAMLError as exc:
        sys.exit("Fatal: Config file cannot be parsed as correct YAML")





class WeatherDaemon(Daemon):
  def run(self):
    while True:
      time.sleep(1)

class WeatherData:

    def __init__(self, t=0, p=0 ):
        self._timestamp = datetime.datetime.utcnow()
        self._temp = t
        self._pressure = p
        self._humidityDHT = 'NaN'
        self._temperatureDHT = 'NaN'
        self._light = 0
        self._winddir = 0
        self._windspeed = 0
        self._rain = 0
        self._dataformatversion = 0.1
        self._DHTsuccess = 0

    @property
    def pressureMillibar(self):
      # Raw is Pascals, divide by 100 to get millibar
      """getting"""
      return "%0.1f" % ((self._pressure/100),)

    @property
    def pressureInchesHG(self):
      # Raw is Pascals, divide by 3389.39 you'll get inches-Hg.
      """getting"""
      return "%0.2f" % ((self._pressure/3389.39),)

    @property
    def dataformatversion(self):
      """getting"""
      return self._dataformatversion

    @property
    def humidityDHT(self):
      """getting"""
      return self._humidityDHT

    @property
    def temperatureDHT(self):
      """getting"""
      return self._temperatureDHT

    @humidityDHT.setter
    def humidityDHT(self, value):
      self._humidityDHT = value

    @temperatureDHT.setter
    def temperatureDHT(self, value):
      self._temperatureDHT = value


    @property
    def tempF(self):
      """getting"""
      return "%0.1f" % ((self._temp*1.8)+32,)

    @property
    def tempC(self):
      """getting"""
      return "%0.1f" % (self._temp,)


    def exportdata(self):
      return [ str(self._timestamp), self.tempF, self.pressureMillibar, self.temperatureDHT, self.humidityDHT, self._light, self._winddir, self._windspeed, self._rain ]



    def describedata(self, v=None):
        v = v or self._dataformatversion
        if v == 0.1:
            return [ "Timestamp UTC",  "BMP Temp F", "BMP Pressure Millibar", "DHT Temp C", "DHT Humidity %",  "Light Count", "Winddir ", "Windspeed Count", "Rain Count"  ]
        else:
            return [v]



if __name__ == '__main__':

  logger = structlog.get_logger()
  GPIO.setwarnings(False)


  logger.info("Loading Configs...")
  cfg = StationConfig('config.yaml')
  #cfg.dumpcfg()

  logger.info("Getting Data Ready:")
  # Get our CSV Writer ready, pass in the Data Header for 1st line
  dataout = CSVWriter("data-"+datetime.date.today().strftime("%Y-%m-%d") + ".csv", WeatherData().describedata())

  #Sensors
  logger.info("Getting Sensors Ready:")
  #print(cfg.configs['bmp183']['pin-sck'])
  bmp = bmp183(cfg.configs['bmp183']['pin-sck'],
               cfg.configs['bmp183']['pin-sdo'],
               cfg.configs['bmp183']['pin-sdi'],
               cfg.configs['bmp183']['pin-cs'])

  datalast = None
  while (1 == 1):

      #print(sorted(list(data._dumprow)))
      bmp.measure_pressure()
      data = WeatherData(bmp.temperature, bmp.pressure )
      print("Temperature: " + data.tempF + " deg F")
      print("Temperature: " + data.tempC + " deg C")
      print("Pressure : " + data.pressureMillibar + " millibar")
      print("Pressure : " + data.pressureInchesHG + " inches-Hg")

      # Every 2 seconds:
      humidity, temperature = Adafruit_DHT.read(11, 6)
      if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
      else:
        if datalast is not None:
              humidity = datalast.humidityDHT
              temperature = datalast.temperatureDHT
        print('Failed to get reading. Try again!')
      data.temperatureDHT = temperature
      data.humidityDHT = humidity

      #Output:
      print("Data:")
      print (list(data.exportdata()))
      dataout.writedata(data.exportdata())

      #print ("Desc: ")
      #print(data.describedata())
      datalast = data
  exit(0);



  daemon = WeatherDaemon('/tmp/weatherdaemon.pid')
  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      logger.info("Starting up...")
      daemon.start()
    elif 'stop' == sys.argv[1]:
      logger.info("Shutting down...")
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      logger.info("Restarting...")
      daemon.restart()
    else:
      print("Unknown command")
      sys.exit(2)
      sys.exit(0)
  else:
    print("usage: %s start|stop|restart" % sys.argv[0])
    sys.exit(2)
  # Date Calcs
  tomorrow = datetime.date.today() + datetime.timedelta(days=1)
  logger.debug("Tomorrow: " + str(tomorrow.month) + " " + str(tomorrow.day))

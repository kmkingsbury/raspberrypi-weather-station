import os, sys
import RPi.GPIO as GPIO
import time
import datetime
import numpy
import logging.config
import csv
import yaml
import structlog

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

    def __init__(self, t, h ):
        self._temp = t
        self._pressure = h
        self._dataformatversion = 0.1
        self._fields = ['tempf', 'pressure', 'dataformatversion']

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
    def tempF(self):
      """getting"""
      return "%0.1f" % ((self._temp*1.8)+32,)

    @property
    def tempC(self):
      """getting"""
      return "%0.1f" % (self._temp,)

    #@temp.setter
    #def temp(self, value):
    #  """setting"""
    #  self._temp = value


if __name__ == '__main__':

  logger = structlog.get_logger()
  GPIO.setwarnings(False)


  logger.info("Loading Configs...")
  cfg = StationConfig('config.yaml')
  #cfg.dumpcfg()
  logger.debug("Sensor Info:")
  #print(cfg.configs['bmp183']['pin-sck'])

  #Sensors
  bmp = bmp183(cfg.configs['bmp183']['pin-sck'],
               cfg.configs['bmp183']['pin-sdo'],
               cfg.configs['bmp183']['pin-sdi'],
               cfg.configs['bmp183']['pin-cs'])

  #data = WeatherData(100,50)
  #print(data.temp)
  #data.temp = 35
  #print(data.temp)
  #print(data.humidity)
  print("Data:")
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
    print('Failed to get reading. Try again!')

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

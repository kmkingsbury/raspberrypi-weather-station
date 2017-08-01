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


# Loggin Stuff
import loggerhelper

from daemon import Daemon

class WeatherDaemon(Daemon):
  def run(self):
    while True:
      time.sleep(1)

class WeatherData:

    def __init__(self, t, h ):
        self.temp = t
        self._humidity = h
        self._dataformatversion = 0.1
        self._fields = ['temp', 'humidity', 'dataformatversion']

    @property
    def humidity(self):
      """getting"""
      return self._humidity

    @property
    def dataformatversion(self):
      """getting"""
      return self._dataformatversion

    @property
    def temp(self):
      """getting"""
      return "%0.1f" % (self._temp,)

    @temp.setter
    def temp(self, value):
      """setting"""
      self._temp = value

    @property
    def _dumprow(self):
      r = []
      r = filter(lambda a: not a.startswith('_') and not callable(getattr(self,a)), dir(self))
      return r

if __name__ == '__main__':

  logger = structlog.get_logger()

  data = WeatherData(100,50)
  print(data.temp)
  data.temp = 35
  print(data.temp)
  print(data.humidity)
  print("Data:")
  print(sorted(list(data._dumprow)))
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

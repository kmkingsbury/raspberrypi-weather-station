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


if __name__ == '__main__':

  logger = structlog.get_logger()


  daemon = Daemon('/tmp/daemon-example.pid')
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



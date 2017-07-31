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


  logger.info("Starting up...")

  # Setup : Read Config YAMl, Open CSV.

  # Date Calcs
  tomorrow = datetime.date.today() + datetime.timedelta(days=1)
  logger.debug("Tomorrow: " + str(tomorrow.month) + " " + str(tomorrow.day))



import sys
import RPi.GPIO as GPIO
import time
import numpy
import structlog
import logging.config
import csv


#Logging:
logger = structlog.get_logger()
LOGLEVEL = 'INFO'


timestamper = structlog.processors.TimeStamper(fmt="iso")
pre_chain = [
    # Add the log level and a timestamp to the event_dict if the log entry
    # is not from structlog.
    structlog.stdlib.add_log_level,
    timestamper,
]
logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "plain": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=False),
                "foreign_pre_chain": pre_chain,
            },
            "colored": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=True),
                "foreign_pre_chain": pre_chain,
            },
        },
        "handlers": {
            "default": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "colored",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.handlers.WatchedFileHandler",
                "filename": "weather.log",
                "formatter": "plain",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default", "file"],
                "level": LOGLEVEL, 
                "propagate": True,
            },
        }
})
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

#logging.basicConfig(
#        format="%(message)s",
#        stream=logfilehandler,
#        level=logging.DEBUG,
#    )
#structlog.configure(
#    processors=[
#        structlog.processors.KeyValueRenderer(
#                key_order=["event"],
#        ),
#    ],
#    context_class=structlog.threadlocal.wrap_dict(dict),
#    logger_factory=structlog.stdlib.LoggerFactory(),
#)
logger.info("Starting up...", somevalue="42")
logger.warning("Test this")
if (1==1):
  logger = logger.bind(earth='flat')
else:
  logger = logger.bind(earth='round')
logger.warning("Event")


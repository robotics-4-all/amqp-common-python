#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config


class LoggingLevel(object):
    DEBUG = logging.DEBUG
    INFO = logging.INFO


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

__LOGGING = dict(
    version=1,
    formatters={
        'f': {'format':
              '[%(asctime)s] - [%(name)s] - [%(levelname)s]: %(message)s',
              'datefmt': '%s'
              }
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
    },
    root={
        'handlers': ['h'],
        'level': logging.DEBUG,
    },
)

logging.config.dictConfig(__LOGGING)

logging.addLevelName(
    logging.WARNING,
    '\033[1;33m%s\033[1;0m' % logging.getLevelName(logging.WARNING)
)

logging.addLevelName(
    logging.ERROR,
    '\033[1;31m%s\033[1;0m' % logging.getLevelName(logging.ERROR)
)

logging.addLevelName(
    logging.DEBUG,
    '\033[1;34m%s\033[1;0m' % logging.getLevelName(logging.DEBUG)
)


def create_logger(namespace):
    """Tiny wrapper around python's logging module"""
    return logging.getLogger(namespace)

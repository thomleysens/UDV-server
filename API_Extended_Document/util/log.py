#!/usr/bin/env python3
# coding: utf8

import logging


def setLogger(logger, level, fileName, mode, formatter):
    logger.setLevel(level)
    fileHandler = logging.FileHandler(fileName, mode=mode)
    formatter = logging.Formatter(formatter)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)


default_formatter = '%(asctime)s [%(levelname)s] \n\t%(message)s'

logger = logging.getLogger('sqlalchemy.engine')

setLogger(logger, logging.INFO, '../info.log', 'w', default_formatter)


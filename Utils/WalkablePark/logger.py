#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
logger
@author: Thomas Leysens
@source: http://sametmax.com/ecrire-des-logs-en-python/
"""

import logging
from logging.handlers import RotatingFileHandler
import time
import datetime
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
 
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
logger.addHandler(stream_handler)


def _get_duration(start):
    """
    
    """
    end=time.time()
    seconds = end-start
    duration = str(datetime.timedelta(seconds=seconds))
    
    return duration
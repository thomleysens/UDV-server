#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 12:45:01 2019

@author: thomas
"""

import progressbar


LOADING_FILES = 5

widgets=[
    ' [',progressbar.ETA(), '] ',
    progressbar.Bar(),
    progressbar.Percentage(),
    progressbar.DynamicMessage('step'),
]
    
bar = progressbar.ProgressBar(
        widgets=widgets,
        redirect_stdout=True
        )
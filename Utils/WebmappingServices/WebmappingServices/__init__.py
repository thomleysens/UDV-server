#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 16:55:19 2019

@author: thomleysens

This module facilitate the access to Webmapping services to get:
    - Data (WFS)
    - Metadata by using Catalog Service Web services

It is mainly based on OWSLib Python library (http://geopython.github.io/OWSLib)
"""

from .get_metadata import CSWGetMetadata
from .get_data import GetWFS
from .geofunctions import gdf_to_geojson
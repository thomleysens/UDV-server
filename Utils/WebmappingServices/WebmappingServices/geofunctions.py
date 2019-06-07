#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:51:04 2019

@author: thomleysens
"""

import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon, Point, LineString
import numpy as np
import json
import geojson
from bokeh.models import GeoJSONDataSource

def gdf_to_geojson(gdf, properties, epsg):
    """
    Description:
    ------------
    
    Transform a GeoDataFrame to a GeoJSON object
    Explanations for reverse and nested lists: 
        - https://tools.ietf.org/html/rfc7946#section-3.1.6
        - https://tools.ietf.org/html/rfc7946#appendix-A.3
    Inspired by: http://geoffboeing.com/2015/10/exporting-python-data-geojson/
    
    Returns:
    --------
    GeoJson object that could be used in bokeh as GeoJsonDataSource
    
    Parameters:
    -----------
    gdf (GeoPandas GeoDataframe): 
        GeoDataframe (polygons) 
    properties (list): 
        list of property columns
    epsg (int):
        EPSG number
    
    """
    
    geojson_ = {
            "type":"FeatureCollection", 
            "features":[],
            "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::{}".format(epsg) } },
            }
#    style_col = ["fill", "fill-opacity", "stroke", "stroke-width", "stroke-opacity"]
    
    if "geometry" in properties:
        properties.remove("geometry")
    
    for line in gdf.itertuples():
        if (isinstance(line.geometry, MultiPolygon)):
            for poly in line.geometry:
                l_poly = []
                for pt in poly.exterior.coords:
                    l_poly.extend([[pt[0],pt[1]]])
                feature = {"type":"Feature",
                       "properties":{},
                       "geometry":{
                               "type":"Polygon",
                               "coordinates":[]
                               },
                       }
                feature["geometry"]["coordinates"] = [list(reversed(l_poly))]
            
                if (properties != []) or (properties is not None):
                    for prop in properties:
                        value_prop = gdf.at[line.Index, prop]
                        if type(value_prop) == np.int64 or type(value_prop) == np.int32:
                            value_prop = int(value_prop)
                        feature["properties"][prop] = value_prop
                
                    geojson_["features"].append(feature)
                else:
                    feature.pop(properties, None)
        elif (isinstance(line.geometry, Polygon)):
            l_poly = []
            for pt in line.geometry.exterior.coords:
                l_poly.extend([[pt[0],pt[1]]])
            feature = {"type":"Feature",
                   "properties":{},
                   "geometry":{
                           "type":"Polygon",
                           "coordinates":[]
                           },
                   "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::{}".format(epsg) } },
                   }
            feature["geometry"]["coordinates"] = [list(reversed(l_poly))]
            if (properties != []) or (properties is not None):
                for prop in properties:
                    value_prop = gdf.at[line.Index, prop]
                    if type(value_prop) == np.int64 or type(value_prop) == np.int32:
                        value_prop = int(value_prop)
                    feature["properties"][prop] = value_prop
            
                geojson_["features"].append(feature)
            else:
                feature.pop(properties, None)
                
        elif (isinstance(line.geometry, LineString)):
            l_poly = [[x[0],x[1]] for x in list(line.geometry.coords)]

            feature = {"type":"Feature",
                   "properties":{},
                   "geometry":{
                           "type":"LineString",
                           "coordinates":[]
                           },
                   "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::{}".format(epsg) } },
                   }
            feature["geometry"]["coordinates"] = l_poly
            if (properties != []) or (properties is not None):
                for prop in properties:
                    value_prop = gdf.at[line.Index, prop]
                    if type(value_prop) == np.int64 or type(value_prop) == np.int32:
                        value_prop = int(value_prop)
                    feature["properties"][prop] = value_prop
            
                geojson_["features"].append(feature)
            else:
                feature.pop(properties, None)
        
        elif (isinstance(line.geometry, Point)):
            l_poly = [[x[0],x[1]] for x in list(line.geometry.coords)]

            feature = {"type":"Feature",
                   "properties":{},
                   "geometry":{
                           "type":"Point",
                           "coordinates":[]
                           },
                   "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::{}".format(epsg) } },
                   }
            feature["geometry"]["coordinates"] = [line.geometry.x,line.geometry.y]
            if (properties != []) or (properties is not None):
                for prop in properties:
                    value_prop = gdf.at[line.Index, prop]
                    if type(value_prop) == np.int64 or type(value_prop) == np.int32:
                        value_prop = int(value_prop)
                    feature["properties"][prop] = value_prop
            
                geojson_["features"].append(feature)
            else:
                feature.pop(properties, None)
    
    return geojson_
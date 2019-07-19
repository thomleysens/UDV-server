#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 11:50:32 2019

@author: thomas
"""

import overpass
import geojson
import json

def get_OSM_poly(
        bbox, 
        key, 
        value, 
        timeout=40,
        endpoint="https://overpass-api.de/api/interpreter"
        ):
    """
    Description
    -----------
    Get OSM data with key/value pair and that is Polygon by making
    queries on Overpass
    
    Return
    ------
    GeoJSON Polygons FeatureCollection
    
    Parameters
    ----------
    - bbox(tuple):
        - bounding box for the query
        - must be (SOUTH, WEST, NORTH, EAST)
        - must be EPSG 4326 (WGS84) projection
        - ex: (45.772, 4.864, 45.778, 4.875)
    - key(str):
        - key for the OSM query
    - value(str):
        - value for the OSM query
    - timeout(int):
        - time in seconds for the timeout
        - default: 40
    - endpoint(str):
        - endpoint for the queries
        - default: "https://overpass-api.de/api/interpreter"
    """
    api = overpass.API(
            timeout=timeout, 
            endpoint=endpoint
            )
    requ =  """
    (
        node["{0}"="{1}"]{2};
        way["{0}"="{1}"]{2};
        relation["{0}"="{1}"]{2};
    );
    (._;>;);
    out geom;
    """.format(key, value,bbox)
    data = api.get(requ, verbosity='geom', responseformat="geojson")
    
    return _from_lines_to_polys(data, key, value)

def _from_lines_to_polys(data, key, value):
    """
    Description
    -----------
    Transform OSM data from LineString to Polygons
    
    Return
    ------
    GeoJSON Polygons FeatureCollection
    
    Parameters
    ----------
    - data(json):
        - json from OSM query
    - key(str):
        - key used for the OSM query
    - value(str):
        - value used for the OSM query
    """
    data = geojson.loads(json.dumps(data))
    features = []
    for feature in data.features:
        if (
            feature.geometry["type"] == "LineString"
        ) and (
            key in feature.properties and feature.properties[key] == value
        ):
            
            geometry = geojson.Polygon(
                [
                    feature.geometry["coordinates"]
                ]
            )
            feature.properties.update({"osm_id":feature.id})
            new_feature = geojson.Feature(
                geometry = geometry,
                properties = feature.properties
            )
            features.append(new_feature)
            
    return geojson.FeatureCollection(features)


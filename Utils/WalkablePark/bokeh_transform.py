#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 09:50:07 2019

@author: thomas
"""

# Transform union_source to Bokeh multi_polygon format
import geojson
import json
from shapely.geometry import shape 
from bokeh.models import GeoJSONDataSource, ColumnDataSource

    
def _to_datasource(poly):
    """
    Return xs and ys coordinates formated for Bokeh multi_polygons 
    glyphs
    """    
    xs, ys = [], []
    if poly.interiors:
        xs.append(poly.exterior.xy[0].tolist())
        ys.append(poly.exterior.xy[1].tolist())
        
        tmp_xs, tmp_ys = [], []
        for interior in poly.interiors:
            tmp_xs.append(interior.xy[0].tolist())
            tmp_ys.append(interior.xy[1].tolist())
            
        xs.extend(tmp_xs)
        ys.extend(tmp_ys)
    else:
        xs.append(poly.exterior.xy[0].tolist())
        ys.append(poly.exterior.xy[1].tolist())
    
    return [xs], [ys]
    

def geojson_to_datasource(geojson_file):
    """
    Get GeoJSON file and return Bokeh ColumnDataSource for multi_polygons 
    """
    xs, ys = [], []
    data = {}
    with open(geojson_file) as f:
        d = json.load(f)
        source = GeoJSONDataSource(
            geojson=json.dumps(d)
        )
        
    multis = geojson.loads(source.geojson)
    for feature in multis.features:
        xs_tmp, ys_tmp = [], []
        shp = shape(feature.geometry)
        
        #Get the geometries
        if shp.geom_type == "MultiPolygon":
            for poly in shp:
                coords = _to_datasource(poly)
                xs_tmp.extend(coords[0])
                ys_tmp.extend(coords[1])
        elif shp.geom_type == "Polygon":
            coords = _to_datasource(shp)
            xs_tmp.extend(coords[0])
            ys_tmp.extend(coords[1])
        
        #Get the properties
        for k,v in feature.properties.items():
            if k not in data:
                data[k] = [v]
            else:
                data[k].append(v)
        
        xs.append(xs_tmp)
        ys.append(ys_tmp)
            
    data["xs"] = xs
    data["ys"] = ys
    
    return ColumnDataSource(data=data)
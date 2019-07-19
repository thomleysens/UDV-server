#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Created on Thu Jun 27 15:45:20 2019
#@author: thomas

"""Get Accessibility and Mask layers.

Usage: get_accessibility_and_mask.py [<json_params>]

  -h --help  Show this screen.
  -i         Parameters JSON file

"""

from jsonschema import validate
from shapely.ops import cascaded_union
from shapely import speedups
import json
import geopandas as gpd
import os
from docopt import docopt
import time

from logger import logger, _get_duration
from schema import SCHEMA
from overpass_methods import get_OSM_poly
from graph_utils import df_to_graph
from isochrone import Accessibility
from get_nearest_points import GetCenterNodes
from graph_utils import graph_to_gdf_points 

speedups.enable()

#Dict of results
results = {}

def get_all_center_nodes(
        polys, 
        points, 
        lat, 
        lng, 
        poly_names=[],
        poly_ids=[]
        ):
    """
    
    """
    if (poly_names != [] and poly_ids !=[]):
        for poly, poly_name, poly_id in zip(polys, poly_names, poly_ids):
            center_nodes = GetCenterNodes(
                poly,
                points,
                poly_name=poly_name,
                poly_id=poly_id,
                lat=lat,
                lng=lng
            ).get_center_nodes()
    
            yield center_nodes
        
    else:
        for poly in polys:
            center_nodes = GetCenterNodes(
                poly,
                points,
                lat=lat,
                lng=lng
            ).get_center_nodes()
    
            yield center_nodes

def erase_file(name):
    """
    
    """
    try:
        os.remove(name)
    except OSError:
        pass

def write_results(results, output_folder, output_format="geopackage"):
    """
    
    """
    encoding = "utf-8"
    if (output_format == "geojson" or output_format == "shapefile"):
        if output_format == "geojson":
            extension = ".geojson"
            driver = "GeoJSON"
        elif output_format == "shapefile":
            extension = ".shp"
            driver = "ESRI Shapefile"
        
        for layer, data in results.items():
            name = os.path.join(
                        output_folder, 
                        str(layer) + extension
                        )
            #Delete file if already exist to avoid errors
            erase_file(name)
            
            data.to_file(
                    name, 
                    driver=driver,
                    encoding=encoding
                    )
        
    elif output_format == "geopackage":
        name = os.path.join(output_folder, "output.gpkg")
        #Delete file if already exist to avoid errors
        erase_file(name)
        
        for layer, data in results.items():
            data.to_file(
                    name,
                    layer = layer,
                    driver="GPKG",
                    encoding=encoding
                    )
            
    elif output_format == "all":
        name_gpkg = os.path.join(output_folder, "output.gpkg")
        #Delete file if already exist to avoid errors
        erase_file(name_gpkg)
        
        for layer, data in results.items():
            name = os.path.join(
                    output_folder, str(layer) + ".shp"
                    )
            erase_file(name)
            data.to_file(
                    name,
                    encoding=encoding
                    )
            
            name = os.path.join(
                    output_folder, str(layer) + ".geojson"
                    )
            erase_file(name)
            data.to_file(
                    name, 
                    driver="GeoJSON",
                    encoding=encoding
                    )
            
            data.to_file(
                    name_gpkg,
                    layer = str(layer),
                    driver="GPKG",
                    encoding=encoding
                    )
        

def run(json_params):
    """
    
    """
    #Load params JSON file
    with open(json_params) as f:
        params = json.load(f)
    
    #Set output
    output_folder = params["output_folder"]
    output_format = params["output_format"]
    
    #Check with schema
    validate(instance=params, schema=SCHEMA)
    
    #Get OSM features
    start = time.time()
    features = get_OSM_poly(
            tuple(params["osm_bbox_query"]),
            params["osm_key_query"],
            params["osm_value_query"]
            )
    
    logger.info(
                """"
                Get OSM features:
                    Total time : {}
                """.format(
                    _get_duration(start)
                )
                )
    
    #Save OSM features as GeoJSON
    gdf_features = gpd.GeoDataFrame.from_features(
            features['features']
            )
    gdf_features.crs = {
            "init":"epsg:{}".format(
                    params["epsg_input"]
                    )
            }
    
    #Add to results
    results[params["output_features_layername"]] = gdf_features
    
    #Import graph from json files and transform to NetworkX MultiDiGraph
    start = time.time()
    G = df_to_graph(
            params["graph_edges_jsonfile"], 
            params["graph_nodes_jsonfile"]
            )
    
    logger.info(
                """"
                Import Graph:
                    Total time : {}
                """.format(
                    _get_duration(start)
                )
                )
    
    #Get center nodes
    ##Get Points GeoDataframe from graph
    start = time.time()
    points = graph_to_gdf_points(
            G,
            params["lat"], 
            params["lon"], 
            params["epsg_graph"],
            )
    
    logger.info(
                """"
                Get Shapely Points from graph:
                    Total time : {}
                """.format(
                    _get_duration(start)
                )
                )
    
    ##Reproject points to metric
    points = points.to_crs(
        {
            "init":"epsg:{}".format(params["epsg_metric"])
        }
    )
    
    ##Reproject polys to metric
    polys_gdf = gdf_features.to_crs(
        {
            "init":"epsg:{}".format(params["epsg_metric"])
        }
    )
    
    ##Get polys as list
    polys_gdf_3857 = polys_gdf.to_crs(
        {
            "init":"epsg:3857"
        }
    )
    polys_3857 = polys_gdf_3857["geometry"].to_list()
    polys = polys_gdf["geometry"].to_list()
    poly_names = polys_gdf["name"].to_list()
    poly_ids = polys_gdf["osm_id"].to_list()
    
    #Get center nodes
    start = time.time()
    center_nodes = get_all_center_nodes(
            polys, 
            points, 
            params["lat"], 
            params["lon"],
            poly_names=poly_names,
            poly_ids=poly_ids
            )
    tmp = []
    for center in center_nodes:
        tmp.extend(center)
        
    logger.info(
                """"
                Get center nodes:
                    Total time : {}
                """.format(
                    _get_duration(start)
                )
                )
    
    ##Delete duplicates
    set_center_nodes = list(set(tmp))
    
    #Get accessibility
    start = time.time()
    access = Accessibility(
            G, 
            params["trip_times"], 
            params["distance_buffer"],
            center_nodes=set_center_nodes,
            )
    access.get_results()
    
    logger.info(
                """"
                Get accessibility:
                    Total time : {}
                """.format(
                    _get_duration(start)
                )
                )    
    
    #Add to results
    results[params["output_isolines_layername"]] = access.lines.vis
    results[params["output_buffered_isolines_layername"]] = access.buffered.vis
    results[params["output_buffered_isolines_union_layername"]] = access.union.vis
    
    #Make Mask layers for each duration 
    start = time.time()
    union_polys = cascaded_union(polys_3857)
    trip_times = []
    for trip_time in params["trip_times"]:
        trip_times.append(trip_time)
        tmp_polys = access.union.vis.loc[
                    (access.union.vis["duration"]>=min(trip_times))
                    & (access.union.vis["duration"]<=max(trip_times))
                    ]["geometry"].tolist()    
        access_polys = cascaded_union(tmp_polys)
        polys = cascaded_union([union_polys, access_polys])
        gdf = gpd.GeoDataFrame(geometry=[polys])
        gdf.crs = {"init":"epsg:3857"}
        
        #Add to results
        results[trip_time] = gdf
        
    logger.info(
                """"
                Making Mask Layers files:
                    Total time : {}
                """.format(
                    _get_duration(start)
                )
                )    
    
    #Write files
    start = time.time()    
    write_results(
            results, 
            output_folder=output_folder, 
            output_format=output_format
            )
    
    logger.info(
                """"
                Writing files:
                    Total time : {}
                """.format(
                    _get_duration(start)
                )
                )
    
    return results

if __name__ == "__main__":
    arguments = docopt(__doc__)
    json_params = arguments["<json_params>"]
    run(json_params)
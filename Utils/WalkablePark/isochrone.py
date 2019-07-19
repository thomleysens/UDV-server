#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 17:43:42 2019

@author: thomas
"""

import osmnx as ox
import geopandas as gpd
import networkx as nx
import numpy as np
from shapely.geometry import Point, LineString
from shapely.ops import cascaded_union
from shapely import speedups
from collections import namedtuple
from bokeh.palettes import Viridis
import time

from logger import _get_duration, logger

speedups.enable()

GeoData = namedtuple("GeoData", ["origin","metric","vis"])
EPSG = namedtuple("EPSG", ["origin", "metric", "vis"])

class Accessibility:
    """
    Description:
    ------------ 
    
    Measure accessibility on a graph (with time as weight on edges) from a 
    list of points and a list of durations. 
    
    Inspired by:
        https://github.com/gboeing/osmnx-examples/blob/master/notebooks/13-isolines-isochrones.ipynb
        http://kuanbutts.com/2017/12/16/osmnx-isochrones/
    
    Returns:
    --------
    Add to the class object:
        - Isolines:
            - object.lines.origin => isolines with origin EPSG
            - object.lines.metric => isolines with metric EPSG
            - object.lines.vis => isolines with visualisation EPSG
        - Buffered isolines:
            - object.buffered.origin => buffered isolines with origin EPSG
            - object.buffered.metric => buffered isolines with metric EPSG
            - object.buffered.vis => buffered isolines with visualisation EPSG
        - Union of buffered isolines by duration:
            - object.union.origin => union of buffered isolines with origin EPSG
            - object.union.metric => union of buffered isolines with metric EPSG
            - object.union.vis => union of buffered isolines with visualisation EPSG
    

            
    Parameters:
    -----------
    pts(list):
        - list of coordinates tuples
    G(NetworkX graph):
        - Graph with time weighted edges
        - MultiDiGraph
    trip_times(list):
        - list of integer values
        - durations value for making isochrones 
    distance_buffer(int):
        - value in meters for buffering isolines
    palette(dict):
        - dict of colors:
            => {1:"#hexcolor1", 2:"hexcolor2"}
        - default: Viridis Bokeh palette
    epsg(dict):
        - dict of EPSG values (origin, metric, visualisation)
        - => metric EPSG is needed to measure buffers in meters, origin EPSG 
        is needed to set the default and visualisation is needed to get 
        elements set for webmapping (example: EPSG 3857)
        - default:
            => epsgs={
                    "origin":"4326",
                    "metric":"2154",
                    "vis":"3857"
                    }
    """
    
    def __init__(
        self, 
        G, 
        trip_times, 
        distance_buffer,
        pts = [],
        palette=Viridis,
        epsgs={
                "origin":"4326",
                "metric":"2154",
                "vis":"3857"
                },
        center_nodes=[]
        ):
        """
        
        """
        if center_nodes == [] and pts != []:
            xs, ys = map(list, zip(*pts))
            self.center_nodes = ox.get_nearest_nodes(
                    G,
                    xs, 
                    ys, 
                    method="kdtree"
                    )
        else:
            self.center_nodes = center_nodes
            
        self.colors = {
            trip_time:color for trip_time,color in zip(
                    trip_times, 
                    palette[len(trip_times)]
                    )
            }
        self.G = G
        self.trip_times = trip_times
        self.distance_buffer = distance_buffer
        self.epsgs = EPSG(
                epsgs["origin"],
                epsgs["metric"],
                epsgs["vis"]
                )
        
    def _make_iso_lines(self):
        """
        Get isolines and returns a GeoDataFrame
        """
        
        l_gdf = []
        
        for center_node in self.center_nodes:
            for trip_time in self.trip_times:
                subgraph = nx.ego_graph(
                        self.G, 
                        center_node, 
                        radius=trip_time, 
                        distance='time'
                        )
                
                node_points = [
                        Point(
                                (
                                        data['x'],
                                        data['y']
                                        )
                                ) for node, data in subgraph.nodes(data=True)
                        ]
                
                if len(node_points) > 1: 
                    nodes_gdf = gpd.GeoDataFrame(
                            {
                                    'id': subgraph.nodes()
                                    }, 
                            geometry=node_points
                            )
                    nodes_gdf = nodes_gdf.set_index('id')
                    df_edges = nx.to_pandas_edgelist(subgraph)
                    df_edges["from"] = df_edges.apply(
                            lambda x: self._get_geom_df(
                                    nodes_gdf,
                                    np.int64(x["source"])
                                    ),
                            axis=1
                            )
                    df_edges["to"] = df_edges.apply(
                            lambda x: self._get_geom_df(
                                    nodes_gdf,
                                    np.int64(x["target"])
                                    ),
                            axis=1
                            )
                    df_edges["line"] = df_edges.apply(
                            lambda x: LineString([x["from"], x["to"]]),
                            axis=1
                            )
                    df_edges["duration"] = trip_time
                    df_edges["color"] = self.colors[trip_time]
                    l_gdf.append(df_edges)
                
        self.gdf = gpd.pd.concat(l_gdf, sort=False)
        
    
    def get_results(self):
        """
        Get isolines GeoDataFrame
        Make buffered isolines (polygons)
        Make union of buffered isolines by duration
        Add these elements to the class
        """        
        start = time.time()
        self._make_iso_lines()
        
        logger.info(
                """"
                Making isolines:
                    Number of nodes: {}
                    Durations values: {}
                    Total time : {}
                """.format(
                    len(self.center_nodes),
                    self.trip_times,
                    _get_duration(start)
                )
                )
        
        gdf_lines = self.gdf[
                ["source", "target", "from", "to", "line", "time", "duration", "color"]
                ]
        
        gdf_lines = gdf_lines.drop_duplicates(
                subset=["source","target"]
                )
        gdf_lines = gdf_lines.rename(
                        columns={'line': 'geometry'}
                        ).set_geometry('geometry')
        gdf_lines.crs = {
                'init': "epsg:{}".format(
                        self.epsgs.origin
                        )
                }
        gdf_lines.to_crs(
                {
                        'init': "epsg:{}".format(
                                self.epsgs.metric
                                )
                        }, 
                inplace=True
                )
                
        gdf_lines.drop(
                ['from','to'], 
                axis=1, 
                inplace=True
                )
        
        start = time.time()
        
        gdf_buffered_lines = gdf_lines[
                ["source", "target","geometry", "color", "duration"]
                ]
        gdf_buffered_lines["polys"] = gdf_buffered_lines.apply(
                        lambda x: x["geometry"].buffer(self.distance_buffer),
                        axis=1
                        )
        
        gdf_buffered_lines.drop(
                ['geometry'], 
                axis=1, 
                inplace=True
                )
        
        gdf_buffered_lines = gdf_buffered_lines.rename(
                columns={'polys': 'geometry'}
                ).set_geometry('geometry')
        
        logger.info(
                """"
                Get buffered isolines:
                    Total time : {}
                """.format(
                    _get_duration(start)
                )
                )
        
        gdf_union = []
        for trip_time in self.trip_times:
            start = time.time()
            
            polys = cascaded_union(
                    gdf_buffered_lines.loc[
                            gdf_buffered_lines["duration"]==trip_time
                            ]["geometry"].values.tolist()
                    ) 
            gdf_buffered_lines_union = gpd.GeoDataFrame(geometry=[polys])
            gdf_buffered_lines_union["duration"] = trip_time
            gdf_buffered_lines_union["color"] = self.colors[trip_time]
            gdf_union.append(gdf_buffered_lines_union)
            
            logger.info(
                """"
                Cascaded union for {} minutes layer:
                    Total time : {}
                """.format(
                    trip_time,
                    _get_duration(start)
                )
                )
        
        gdf_union = gpd.pd.concat(gdf_union, sort=False)
    
        self.lines = GeoData(
                self._change_crs(
                        gdf_lines, 
                        self.epsgs.origin
                        ),
                gdf_lines,
                self._change_crs(
                    gdf_lines, 
                    self.epsgs.vis
                    )
                )
        
        gdf_union.crs = {
                'init': "epsg:{}".format(
                        self.epsgs.metric
                        )
                }
        self.union = GeoData(
                self._change_crs(
                        gdf_union, 
                        self.epsgs.origin
                        ),
                gdf_union,
                self._change_crs(
                    gdf_union, 
                    self.epsgs.vis
                    )
                )
                
        gdf_buffered_lines.crs = {
                'init': "epsg:{}".format(
                        self.epsgs.metric
                        )
                }
        self.buffered = GeoData(
                self._change_crs(
                        gdf_buffered_lines, 
                        self.epsgs.origin
                        ),
                gdf_buffered_lines,
                self._change_crs(
                    gdf_buffered_lines, 
                    self.epsgs.vis
                    )
                )
        
    def _change_crs(self, gdf, crs):
        """
        Change the CRS/EPSG of a GeoDataFrame
        """
        gdf.to_crs(
                {
                        'init': "epsg:{}".format(crs)
                        }, 
                inplace=True
                )
        
        return gdf

    def _get_geom_df(self, gdf, node):
        """
        Description:
        ------------
        Get geometry of a node source or target
        Used to make LineStrings
        
        Parameters:
        -----------
        gdf(GeoDataFrame):
            - GeoDataFrame
        node(str): 
            - source or target graph node
        
        """
        
        return gdf.at[(node, "geometry")]
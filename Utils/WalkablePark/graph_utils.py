#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:15:41 2019

@author: thomas
"""

from pyproj import Transformer
from shapely.geometry import Point
from collections import namedtuple
import pandas as pd
import geopandas as gpd
import networkx as nx
import json
import numpy as np

Points = namedtuple("Points",["coordinates","geometry"])


def reproject_points(pts, epsg_in, epsg_out):
    """
    Description
    ------------
    
    Reproject points with pyproj.Transformer
    
    Returns
    --------
    
    Namedtuple Points object with:
        - coordinates: tuple with 2 lists (xs and ys)
        - geometry: list of Shapely Points
    
    Parameters
    -----------
    
    - pts (list of tuples coordinates):
        - List of coordinates
        - ex: [(4.56, 45.8), (4.8, 46.29)]
    - epsg_in (int):
        - Input EPSG
        - ex: 4326
    - epsg_out (int):
        - Output EPSG
        - ex: 2154
    
    """
    
    transformer = Transformer.from_proj(epsg_in, epsg_out)
    xcoords,ycoords = map(list,zip(*pts))
    
    coords = transformer.transform(xcoords, ycoords)
    
    points = [Point(x, y) for x,y in zip(coords[0], coords[1])]
    
    return Points(
            [
                    (x,y) for x,y in zip(
                            coords[0], 
                            coords[1]
                            )
                    ], 
            points
            )


def graph_to_df(graph, edges_path, nodes_path):
    """
    Description
    ------------
    Write json files with edges and nodes
    
    Parameters
    -----------
    - graph(Networkx graph): 
        graph with geometries
    - edges_path(str): 
        complete path with filename for edges
    - nodes_path(str): 
        complete path with filename for nodes
    
    """
    #Get edges and write GeoJSON
    df_edges = nx.to_pandas_edgelist(graph)
    df_edges = df_edges[["source", "target", "time"]]
    df_edges.to_json(edges_path, force_ascii=True, orient="records")

    #Get nodes (get 'x' and 'y' for futur center_nodes operations)
    # and write json to get a dict of nodes attributes
    l_nodes = list(graph.nodes(data=True))
    nodes = dict(l_nodes)
    with open(nodes_path, "w") as fp:
        json.dump(nodes, fp, ensure_ascii=False)
    
def df_to_graph(edges_path, nodes_path, source="source", target="target"):
    """
    Description
    ------------
    Get edges and nodes json files and return G, a Networkx graph
    
    Returns
    --------
    Graph G
    
    Parameters
    -----------
    - edges_path(str): 
        complete path with filename for edges
    - nodes_path(str): 
        complete path with filename for nodes
    - source(str): 
        name of source field
        default: "source"
    - target(str): 
        name of target field
        default: "target"
    """
    G = nx.Graph()
    df_edges = pd.read_json(edges_path, orient="records")
    dict_edges = df_edges.to_dict(orient="list")
    edges = pd.DataFrame(dict_edges)
    G = nx.from_pandas_edgelist(edges, source=source, target=target, edge_attr=True)
    
    with open(nodes_path, "r") as fp:
        attrs = json.load(fp)
    
    new_attrs = {}
    for key,value in attrs.items():
        new_attrs[np.int64(key)] = value
    
    nx.set_node_attributes(G, new_attrs)
    
    return G

def graph_with_time(G, walk_distance):
    """
    Description
    ------------
    Get edges and nodes json files
    
    Returns
    --------
    Networkx Graph with time distance based on walk distance speed
    
    Parameters
    """
    meters_per_minute = walk_distance/60

    for u, v, k, data in G.edges(data=True, keys=True):
        data['time'] = data['length'] / meters_per_minute
    
    return G

def graph_to_gdf_points(G, x, y, epsg):
    """
    Description
    ------------
    From Networkx Graph nodes from OSM data, make a GeoDataFrame with Points
    
    Returns
    --------
    Points GeoDataFrame
    
    Parameters
    -----------
    - G (NetworkX graph):
        - Graph based on OSM data (build with Osmnx library)
    - x(str):
        - name of column with x coordinates
    - y(str):
        - name of column with y coordinates
    - epsg(str):
        - EPSG of coordinates
        
    """
    df = pd.DataFrame.from_dict(
            dict(
                    list(
                            G.nodes(data=True)
                            )
                    ), 
            orient="index"
            )
    df["geometry"] = df.apply(lambda x: Point(x["x"], x["y"]), axis=1)
    gdf = gpd.GeoDataFrame(df)
    gdf.set_geometry("geometry")
    gdf.crs = {"init":"epsg:{}".format(epsg)}
    
    return gdf
    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 16:58:37 2019

@author: thomas
"""

from logger import logger

"""
Minimum value in meters for the buffering of the polygon
"""
BUFF_DIST = 2


class GetCenterNodes:
    """
    Description
    ------------
    Get nodes that are included in a buffer of a polygon
    
    Returns
    --------
    Selected nodes
    
    Parameters
    -----------
    - G (NetworkX graph):
        - Graph based on OSM data (build with Osmnx library)
    - polygon():
        - Shapely polygon
    - epsg(int):
        - Projection CRS of polygons
    - epsg_metric(int):
        - transition epsg for the buffering process
    - epsg_graph(int):
        - CRS of graph
        - default: 4326
    - lat(str):
        - name of column with x coordinates
        - default: x
    - lng(str):
        - name of column with y coordinates
        - default: y
    """

    def __init__(self, 
                 polygon,
                 points,
                 poly_name = "No name",
                 poly_id = 0,
                 lat="x", 
                 lng="y"
                 ):
        """
        Init
        """
        self.points = points
        self.polygon = polygon
        
        self.buff_dist = BUFF_DIST
        self.buff_dist_init = BUFF_DIST
        
        self.sindex = points.sindex
        
        self.poly_name = poly_name
        self.poly_id = poly_id
        
 
    def _get_buffer_ring(self):
        """
        
        """
        buffer = self.polygon.buffer(self.buff_dist)
        self.poly = buffer.difference(self.polygon)
 
    def _get_and_check(self):
        """
        
        """
        self._get_buffer_ring()
        possible_matches_index = list(self.sindex.intersection(self.poly.bounds))
        possible_matches = self.points.iloc[possible_matches_index]
        precise_matches = possible_matches[possible_matches.intersects(self.poly)]
        
        return list(
                precise_matches.index
                )

    def get_center_nodes(self):
        """
        
        """
        center_nodes = self._get_and_check()
        # Check to get at least 1 node
        ## add 2 meters to self.buff_dist when this condition
        ## is not fullfilled
        while len(center_nodes) < 1:
            self.buff_dist += BUFF_DIST
            center_nodes = self._get_and_check()
            if self.buff_dist >= 50:
                logger.warning(
                """
                Name: {}, OSM_ID: {}:
                Maximum distance reached: {} meter(s).
                No graph nodes found. 
                """.format(
                            self.poly_name, 
                            self.poly_id,
                            self.buff_dist
                            )
                    )
                break
            
        logger.info(
        """
        {}:
        Distance used for buffer: {} meter(s)
        """.format(
                    self.poly_name, self.buff_dist
                    )
            )
        return center_nodes
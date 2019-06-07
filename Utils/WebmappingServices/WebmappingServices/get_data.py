#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 12:48:01 2019

@author: thomleysens
"""

from requests import Request, get
from json import dump

class GetWFS:
    """
    Description:
    ------------
    
    Get WFS and returns URL
    Write GML and GeoJSON
    
    Parameters:
    -----------
    
        url(str): 
            - url to access WFS service
            - ex: "https://download.data.grandlyon.com/wfs/grandlyon"
            
        name(str): 
            - name of the WFS element
            - ex: "pvo_patrimoine_voirie.pvostationnementvelo"
            
        version(str):
            - WFS version number
            - default: "2.0.0" 
    """
    def __init__(self,url, name,version="2.0.0"):
        
        self.url = url
        self.service="WFS"
        self.version=version
        self.request = "GetFeature"
        self.typeName = name

    def request_url(self):
        """
        Description:
        ------------
        
        Get the URL request
        """
        #GeoJSON
        self.request_GeoJSON = Request(
                'GET', 
                self.url, 
                params=dict(
                        service=self.service,
                        version=self.version,
                        typeName=self.typeName,
                        request=self.request,
                        outPutFormat="GEOJSON"
                        )
                ).prepare().url
                
        #GML
        self.request_GML = Request(
                'GET', 
                self.url, 
                params=dict(
                        service=self.service,
                        version=self.version,
                        typeName=self.typeName,
                        request=self.request,
                        outPutFormat="GML"
                        )
                ).prepare().url
    
    def get_GML(self, filename):
        """
        Description:
        ------------
        
        Writes a GML file from WFS request
        
        Parameters:
        -----------
        
            filename(str): filepath of GML file
        """
        with open(filename, "wb") as out:
            out.write(
                bytes(
                    get(self.request_GML).text, 
                    "UTF-8"
                )
            )
        
    def get_GeoJSON(self, filename):
        """
        Description:
        ------------
        
        Writes a GeoJSON file from WFS request
        
        Parameters:
        -----------
        
            filename(str): filepath of GeoJSON file
        """        
        with open(filename,"w", encoding='UTF-8') as f:
                dump(
                        get(self.request_GeoJSON).json(),
                        f, 
                        ensure_ascii=False,
                        indent=4
                        )
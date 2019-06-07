#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:59:16 2019

author: thomleysens
"""

from owslib.wfs import WebFeatureService
from urllib.request import urlopen
from xml.etree import ElementTree as ET
from xmljson import parker as pk
import re
from json import dumps, loads, dump
from datetime import datetime
from owslib.csw import CatalogueServiceWeb
from owslib.fes import PropertyIsEqualTo, PropertyIsLike, BBox
from os import path
import geopandas as gpd

from .get_data import GetWFS

class CSWGetMetadata:
    """
    Description:
    ------------
    
    Get metadata with CSW service and write a JSON file for each element 
    
    Returns:
    --------
    
    Dict of metadata 
    
    Parameters:
    -----------
    
        csw_url(str): 
            URL of CSW service
        query_(str): 
            query for metadata search
        directory(str): 
            directory path for writing JSON files
        method(str): 
            - search method,
            - default: "csw:AnyText" 
        query_type(str): 
            - query type
            =>"equal" or "like"
            - default: "like"
        bbox(list):
            - list of bouding box limits
            => [xmin, ymin, xmax, ymax]
            => [left, bottom, right, top]
            => tile calculator tool available here: 
                http://tools.geofabrik.de/calc/
            - default: []
        esn(str):
            - details level, element set name
            - => "full", "summary", "brief"
            - default: "full"
        WFS_version(str):
            - version of WFS
            - default: "2.0.0"
    """
    
    def __init__(self,
                 csw_url,
                 query,
                 directory,
                 method='csw:AnyText', 
                 query_type="equal",
                 bbox=[],
                 esn="full",
                 WFS_version="2.0.0"
                 ):
        
        self.csw = CatalogueServiceWeb(csw_url)
        self.directory = directory
        self.WFS_version = WFS_version
            
        if query_type == "equal":
            query = PropertyIsEqualTo(method, query)
        elif query_type == "like":
            query = PropertyIsLike(method, '%{}%'.format(query))
        
        if bbox != []:
            bbox = BBox(bbox)
            constraints = [bbox, query]
        else:
            constraints = [query]
        self.csw.getrecords2(
                constraints=constraints,
                esn=esn
                )
        
        self.dict_={}
    
    def _bbox_crs(self, bbox):
        """
        Description:
        ------------
        
        Get the bounding box object and returns epsg and bbox array that 
        can be JSON serialized
        
        Returns: 
        --------
        
        dict with EPSG, and BBOX
        
        Parameters:
        -----------
        bbox: 
            Bounding Box object
        """
        if bbox is None:
            epsg = ""
            bbox = []
        else:
            epsg = str(bbox.crs).split(":")[-1].replace(")","")
            bbox = [bbox.minx, bbox.miny, bbox.maxx, bbox.maxy]
        
        return {
                "EPSG":epsg,
                "BBOX":[float(element) for element in bbox]
                }
        
    def _get_geom(self, WFS_name, WFS_url):
        """
        
        """
        wfs = GetWFS(
                WFS_url,
                name=WFS_name,
                version=self.WFS_version
            )
    
        wfs.request_url()
        try:
            gdf = gpd.read_file(wfs.request_GeoJSON)
            geom_type = gdf.geom_type[0]
        except:
            geom_type = None
            
        return geom_type
    
    def _get_metadata(self):
        """
        Get metadata from records and update self.dict_
        """
        for rec in self.csw.records:
            r = self.csw.records[rec]
                    
            for attr, value in vars(r).items():
                if attr != "xml":
                    if attr == "bbox":
                        value = self._bbox_crs(value)
                    if attr == "uris":
                        for uri in value:
                            if uri["protocol"] == "OGC:WFS":
                                WFS_name = uri["name"]
                                WFS_url = uri["url"]
                    if r.title in self.dict_:
                        self.dict_[r.title].update(
                                {attr:value}
                                )
                    else:
                        self.dict_[r.title] = {attr:value}
                        
            self.dict_[r.title].update(
                    {
                            "WFS_name":WFS_name,
                            "WFS_url":WFS_url,
                            "geom_type":self._get_geom(
                                    WFS_name,
                                    WFS_url
                                    )
                            }
                    )
            
    def get_json(self):
        """
        Description:
        ------------
        
        Write JSON files and returns dict
        """
        self._get_metadata()
        
        for key,value in self.dict_.items():
            filename = path.join(self.directory, key + ".json")
            with open(filename,"w", encoding='UTF-8') as f:
                dump(
                        value,
                        f, 
                        ensure_ascii=False,
                        indent=4
                        )
        
        
        
#class WFSGetMetadata:
#    def __init__(self, wfs_url, version, content, replacements):
#        """
#        
#        """
#        self.wfs = WebFeatureService(wfs_url, version=version)
#        self.content = self.wfs.contents[content]
#        self.root = ET.parse(
#                urlopen(
#                        self.content.metadataUrls[0]['url']
#                        )
#                ).getroot()
#        self.replacements = replacements
#                
#    def multireplace(self, string, replacements):
#        """
#        Source: https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
#        Given a string and a replacement map, it returns the replaced string.
#        :param str string: string to execute replacements on
#        :param dict replacements: replacement dictionary {value to find: value to replace}
#        :rtype: str
#        """
#        # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
#        # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
#        # 'hey ABC' and not 'hey ABc'
#        substrs = sorted(replacements, key=len, reverse=True)
#    
#        # Create a big OR regex that matches any of the substrings to replace
#        regexp = re.compile('|'.join(map(re.escape, substrs)))
#    
#        # For each match, look up the new string in the replacements
#        return regexp.sub(lambda match: replacements[match.group(0)], string)
#        
#    def get_metadata(self):
#        """
#        
#        """
#        dict_ = loads(
#                self.multireplace(
#                    dumps(
#                        pk.data(self.root)
#                    ), 
#                    self.replacements
#                )
#            )
#                    
#        metadata = {}
#        
#        for key, value in dict_.items():
#            metadata["fileIdentifier"] = value["fileIdentifier"]["CharacterString"]
#            metadata["language"] = value["language"]["CharacterString"]
#            metadata["parentIdentifier"] = value["parentIdentifier"]["CharacterString"]
#            metadata["dateStamp"] = datetime.strptime(
#                    value["dateStamp"]["DateTime"], 
#                    '%Y-%m-%dT%H:%M:%S'
#                    )
#            for x in value["referenceSystemInfo"]:
#                if type(x["MD_ReferenceSystem"]) is dict:
#                    metadata["referenceSystemInfo"] = x["MD_ReferenceSystem"]["referenceSystemIdentifier"]["RS_Identifier"]["code"]["CharacterString"]
#
#            ident = value["identificationInfo"]["MD_DataIdentification"]
#            metadata["date"] = datetime.strptime(
#                    ident["citation"]["CI_Citation"]["date"]["CI_Date"]["date"]["Date"], 
#                    '%Y-%m-%d'
#                    )
#            metadata["title"] = ident["citation"]["CI_Citation"]["title"]["CharacterString"]
#            metadata["abstract"] = ident["abstract"]["CharacterString"]
#            metadata["CI_ResponsibleParty"] = ident["pointOfContact"]["CI_ResponsibleParty"]["individualName"]["CharacterString"]
#            metadata["organisationName"] = ident["pointOfContact"]["CI_ResponsibleParty"]["organisationName"]["CharacterString"]
#            metadata["MD_RestrictionCode"] = ident["resourceConstraints"]["MD_LegalConstraints"]["accessConstraints"]["MD_RestrictionCode"]
#            metadata["MD_SpatialRepresentationTypeCode"] = ident["spatialRepresentationType"]["MD_SpatialRepresentationTypeCode"]
#            metadata["topicCategory"] = [x["MD_TopicCategoryCode"] for x in ident["topicCategory"]]
#            bbox = ident["extent"]["EX_Extent"]["geographicElement"]["EX_GeographicBoundingBox"]
#            metadata["westBoundLongitude"] = bbox["westBoundLongitude"]["Decimal"]
#            metadata["eastBoundLongitude"] = bbox["eastBoundLongitude"]["Decimal"]
#            metadata["southBoundLatitude"] = bbox["southBoundLatitude"]["Decimal"]
#            metadata["northBoundLatitude"] = bbox["northBoundLatitude"]["Decimal"]
#            ressources = value["distributionInfo"]["MD_Distribution"]["transferOptions"]["MD_DigitalTransferOptions"]["onLine"]
#            metadata["CI_OnlineResource"] = [x["CI_OnlineResource"]["linkage"]["URL"] for x in ressources]
#            metadata["dataQualityInfo"] = value["dataQualityInfo"]["DQ_DataQuality"]["lineage"]["LI_Lineage"]["statement"]["CharacterString"]
#        
#        return metadata
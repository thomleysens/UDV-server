#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:06:09 2019

@author: thomas
"""

from flask import request
from flask_api import FlaskAPI, status, exceptions

from get_metadata import CSWGetMetadata as CSW

app = FlaskAPI(__name__)

#for first test, hard writing of CSW URL API
csw_url = "https://download.data.grandlyon.com/catalogue/srv/fre/csw"

@app.route("/csw/", methods=['GET'])
def get_WFS_dict():
    """
    
    """
    requ = str(request.args.get("request"))
    bbox = str(request.args.get("bbox")).split(",")
    bbox = [float(x) for x in bbox]

    csw = CSW(csw_url, requ, bbox=bbox)
    csw.get_metadata()
    
    if not csw.dict_:
        raise exceptions.NotFound()
    else:
        dict_ = {}
            
        for element,metadata in csw.dict_.items():
            dict_[element] = {
                    "WFS_url":metadata["WFS_url"],
                    "WFS_name":metadata["WFS_name"],
                    "geom_type":metadata["geom_type"]
                    }
    
    return dict_
    

if __name__ == "__main__":
    app.run(debug=True)
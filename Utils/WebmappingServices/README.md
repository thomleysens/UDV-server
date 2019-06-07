# WebmappingServices

Created on Thu Jun  6 16:55:19 2019

@author: thomleysens

This module facilitate the access to Webmapping services to get:
    - Data (WFS)
    - Metadata by using Catalog Service Web services

It is mainly based on OWSLib Python library (http://geopython.github.io/OWSLib)

Examples can be found in the Jupyter notebook and here (*nbviewer notebook*):

https://nbviewer.jupyter.org/github/MEPP-team/UDV-server/blob/dev/Utils/WebmappingServices/Get%20and%20visualise%20data%20%26%20metadata.ipynb

# WebmappingServices.get_data

Created on Tue Jun  4 12:48:01 2019

@author: thomleysens

## GetWFS
```python
GetWFS(self, url, name, version='2.0.0')
```

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

### request_url
```python
GetWFS.request_url(self)
```

Description:
------------

Get the URL request

### get_GML
```python
GetWFS.get_GML(self, filename)
```

Description:
------------

Writes a GML file from WFS request

Parameters:
-----------

    filename(str): filepath of GML file

### get_GeoJSON
```python
GetWFS.get_GeoJSON(self, filename)
```

Description:
------------

Writes a GeoJSON file from WFS request

Parameters:
-----------

    filename(str): filepath of GeoJSON file

# WebmappingServices.get_metadata

Created on Mon Jun  3 12:59:16 2019

author: thomleysens

## CSWGetMetadata
```python
CSWGetMetadata(self, csw_url, query, directory, method='csw:AnyText', query_type='equal', bbox=[], esn='full', WFS_version='2.0.0')
```

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

### get_json
```python
CSWGetMetadata.get_json(self)
```

Description:
------------

Write JSON files and returns dict


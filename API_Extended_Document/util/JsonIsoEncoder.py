#!/usr/bin/env python3
# coding: utf8

from flask.json import JSONEncoder
from datetime import date


class JsonIsoEncoder(JSONEncoder):
    """
    This class is used to replace the default Flask JSON encoder.
    It performs the same operations, except for the `date` objects (from
    datetime). Those are serialized following the ISO 8601 norm, instead
    of the default RFC 1123.
    """

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


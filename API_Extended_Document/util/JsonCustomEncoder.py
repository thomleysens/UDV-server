#!/usr/bin/env python3
# coding: utf8

from flask.json import JSONEncoder
from datetime import date
from enum import Enum


class JsonCustomEncoder(JSONEncoder):
    """
    This class is used to replace the default Flask JSON encoder.
    It performs the same operations, except for 2 types of object. The `date`
    objects (from datetime) are serialized following the ISO
    8601 norm, instead of the default RFC 1123. For instances of `Enum`, the
    encoder simply takes the value of the instance.
    """

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            elif isinstance(obj, Enum):
                return obj.name
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, Float
from sqlalchemy import ForeignKey

from util.util import Base


class Visualisation(Base):
    __tablename__ = "visualisation"

    id = Column(Integer, ForeignKey('extended_document.id'), primary_key=True, )
    quaternionX = Column(Float)
    quaternionY = Column(Float)
    quaternionZ = Column(Float)
    quaternionW = Column(Float)
    positionX = Column(Float)
    positionY = Column(Float)
    positionZ = Column(Float)

    def update(self, newValues):
        for attKey, attVal in newValues.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)

    def getAllAttr(self):
        return {i for i in dir(self) if not (i.startswith('_') or callable(getattr(self, i)) or i == "metadata")}

    def serialize(self):
        objectSerialized = {}
        for attr in self.getAllAttr():
            objectSerialized[attr] = getattr(self, attr)
        return objectSerialized


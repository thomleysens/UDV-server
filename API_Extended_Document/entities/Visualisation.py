#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, Float
from sqlalchemy import ForeignKey

from util.db_config import Base


class Visualisation(Base):
    __tablename__ = "visualisation"

    id = Column(Integer, ForeignKey('extended_document.id'),
                primary_key=True, )
    quaternionX = Column(Float)
    quaternionY = Column(Float)
    quaternionZ = Column(Float)
    quaternionW = Column(Float)
    positionX = Column(Float)
    positionY = Column(Float)
    positionZ = Column(Float)

    def update(self, new_values):
        for attKey, attVal in new_values.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)
        return self

    def get_all_attr(self):
        return {i for i in dir(self)
                if not (i.startswith('_')
                        or callable(getattr(self, i))
                        or i == "metadata")}

    def serialize(self):
        serialized_object = {}
        for attr in self.get_all_attr():
            serialized_object[attr] = getattr(self, attr)
        return serialized_object

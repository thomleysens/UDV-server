#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from util.db_config import Base
from entity.MetaData import MetaData
from entity.Visualisation import Visualisation


class ExtendedDocument(Base):
    __tablename__ = "extended_document"

    id = Column(Integer, primary_key=True)
    metaData = relationship("MetaData",
                            uselist=False,
                            cascade="all, delete-orphan")
    visualization = relationship("Visualisation",
                                 uselist=False,
                                 cascade="all, delete-orphan")

    def __init__(self):
        self.metaData = MetaData()
        self.visualization = Visualisation()

    def get_all_attr(self):
        return {i for i in dir(self)
                if not (i.startswith('_')
                        or callable(getattr(self, i))
                        or i == "metadata")}

    def serialize(self):
        serialized_object = {}
        for attr in self.get_all_attr():
            try:
                serialized_object[attr] = getattr(self, attr).serialize()
            except AttributeError:
                serialized_object[attr] = getattr(self, attr)
        return serialized_object

    def update(self, attributes):
        self.metaData.update(attributes)
        self.visualization.update(attributes)

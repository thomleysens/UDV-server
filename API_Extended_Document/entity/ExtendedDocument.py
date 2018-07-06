#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from util.util import Base


class ExtendedDocument(Base):
    __tablename__ = "extended_document"

    id = Column(Integer, primary_key=True)
    metaData = relationship("MetaData",
                            uselist=False,
                            cascade="all, delete-orphan")
    visualisation = relationship("Visualisation",
                                 uselist=False,
                                 cascade="all, delete-orphan")

    def getAllAttr(self):
        return {i for i in dir(self) if not (i.startswith('_') or callable(getattr(self, i)) or i == "metadata")}

    def serialize(self):
        objectSerialized = {}
        for attr in self.getAllAttr():
            try:
                objectSerialized[attr] = getattr(self, attr).serialize()
            except AttributeError:
                objectSerialized[attr] = getattr(self, attr)
        return objectSerialized

    def update(self, attributes):
        self.metaData.update(attributes)
        self.visualisation.update(attributes)

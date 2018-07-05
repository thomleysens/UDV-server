#!/usr/bin/env python3
# coding: utf8

import json
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from util.util import Base


class ExtendedDocument(Base):
    __tablename__ = "extended_document"

    id = Column(Integer, primary_key=True)
    metaData = relationship("MetaData",
                            uselist=False,
                            back_populates="extendedDocument",
                            cascade="all, delete-orphan")
    visualisation = relationship("Visualisation",
                                 uselist=False,
                                 back_populates="extendedDocument",
                                 cascade="all, delete-orphan")

    def __str__(self):
        return "{document:  {" + \
               "id : " + str(self.id) + ", " + \
               str(self.metaData) + ", " + \
               str(self.visualisation) + "}}"

    def serialize(self):
        return json.dumps({'aDocument': {'type': "document", "properties": {"id": self.id, "metaData": self.metaData.serialise()}}}, indent=2)

    def update(self, attributes):
        self.metaData.update(attributes)
        self.visualisation.update(attributes)

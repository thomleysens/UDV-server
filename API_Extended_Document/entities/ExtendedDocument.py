#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from entities.MetaData import MetaData
from entities.Visualisation import Visualisation
from util.db_config import Base
from util.serialize import serialize

class ExtendedDocument(Base):
    __tablename__ = "extended_document"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer,
                    ForeignKey("user.id"),
                    nullable=False)

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
            serialized_object[attr] = serialize(getattr(self, attr))
        return serialized_object

    def update(self, attributes):
        self.metaData.update(attributes)
        self.visualization.update(attributes)
        for attKey, attVal in attributes.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)
        return self

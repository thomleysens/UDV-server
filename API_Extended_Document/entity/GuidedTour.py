#!/usr/bin/env python3
# coding: utf8

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from entity.DocumentTour import DocumentTour
from util.db_config import Base
from util.serialize import serialize


class GuidedTour(Base):
    __tablename__ = "guided_tour"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    extendedDocs = relationship('ExtendedDocument',
                                secondary=DocumentTour)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def get_attr(cls, attr_name):
        if hasattr(cls, attr_name):
            return getattr(cls, attr_name)
        return None

    def get_all_attr(self):
        return {i for i in dir(self)
                if not (i.startswith('_')
                        or callable(getattr(self, i))
                        or i == "metadata")}

    def serialize(self):
        serialized_object = {}
        for attr in self.get_all_attr():

            try:
                serialized_object[attr] = serialize(getattr(self, attr))
            except AttributeError:
                serialized_object[attr] = getattr(self, attr)
        return serialized_object

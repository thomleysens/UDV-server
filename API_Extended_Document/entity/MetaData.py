#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

from util.db_config import Base


class MetaData(Base):
    __tablename__ = "metadata"

    id = Column(Integer, ForeignKey('extended_document.id'),
                primary_key=True)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(String, nullable=False)
    refDate = Column(String)
    publicationDate = Column(String)
    type = Column(String)
    link = Column(String)
    originalName = Column(String)

    def update(self, new_values):
        for attKey, attVal in new_values.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)
        return self

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
            serialized_object[attr] = getattr(self, attr)
        return serialized_object

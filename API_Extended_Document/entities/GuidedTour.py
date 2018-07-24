#!/usr/bin/env python3
# coding: utf8

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from util.db_config import Base
from util.serialize import serialize


class GuidedTour(Base):
    __tablename__ = "guided_tour"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    extendedDocs = relationship('ExtendedDocGuidedTour',
                                cascade="all, delete-orphan")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def update(self, new_values):
        for attKey, attVal in new_values.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)
        return self

    def update_document(self, doc_position, new_values):
        for document in self.extendedDocs:
            if document.doc_position == doc_position:
                return document.update(new_values)

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
            serialized_object[attr] = serialize(getattr(self, attr))
        return serialized_object

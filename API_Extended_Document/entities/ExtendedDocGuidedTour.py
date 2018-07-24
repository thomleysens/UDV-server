#!/usr/bin/env python3
# coding: utf8

from json import dumps

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from util.db_config import Base
from util.serialize import serialize


class ExtendedDocGuidedTour(Base):
    __tablename__ = "extended_doc_guided_tour"

    id = Column(Integer, primary_key=True)
    tour_id = Column(Integer,
                     ForeignKey("guided_tour.id"))

    # Cannot deletion on relationship because it's
    doc_id = Column(Integer,
                    ForeignKey("extended_document.id",
                               ondelete="CASCADE"))

    doc_position = Column(Integer)
    document = relationship("ExtendedDocument")
    text1 = Column(String)
    text2 = Column(String)
    title = Column(String)

    def __init__(self, tour_id, doc_id, doc_position):
        self.tour_id = tour_id
        self.doc_id = doc_id
        self.doc_position = doc_position

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
            serialized_object[attr] = serialize(getattr(self, attr))
        return serialized_object

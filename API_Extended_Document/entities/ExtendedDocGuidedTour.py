#!/usr/bin/env python3
# coding: utf8
from json import dumps

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from util.db_config import Base
from util.serialize import serialize


class ExtendedDocGuidedTour(Base):
    __tablename__ = "extended_doc_guided_tour"

    id = Column(Integer, primary_key=True)
    tour_id = Column(Integer,
                     ForeignKey("guided_tour.id"))
    doc_id = Column(Integer,
                    ForeignKey("extended_document.id",
                               ondelete="CASCADE"))

    doc_position = Column(Integer)
    document = relationship("ExtendedDocument")

    def __init__(self, tour_id, doc_id, doc_position):
        self.tour_id = tour_id
        self.doc_id = doc_id
        self.doc_position = doc_position

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

#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from util.db_config import Base

from entities.Entity import Entity


class DocumentGuidedTour(Base, Entity):
    __tablename__ = "document_guided_tour"

    id = Column(Integer, primary_key=True)
    tour_id = Column(Integer,
                     ForeignKey("guided_tour.id"))

    # Cannot deletion on relationship because it's
    doc_id = Column(Integer,
                    ForeignKey("document.id",
                               ondelete="CASCADE"))

    doc_position = Column(Integer)
    document = relationship("Document")
    text1 = Column(String)
    text2 = Column(String)
    title = Column(String)

    def __init__(self, tour_id, doc_id, doc_position):
        self.tour_id = tour_id
        self.doc_id = doc_id
        self.doc_position = doc_position

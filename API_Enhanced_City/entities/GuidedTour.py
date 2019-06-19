#!/usr/bin/env python3
# coding: utf8

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from util.db_config import Base
from entities.Entity import Entity


class GuidedTour(Entity, Base):
    __tablename__ = "guided_tour"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    extendedDocs = relationship('DocumentGuidedTour',
                                cascade="all, delete-orphan")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def update_document(self, doc_position, new_values):
        for document in self.extendedDocs:
            if document.doc_position == doc_position:
                return document.update(new_values)

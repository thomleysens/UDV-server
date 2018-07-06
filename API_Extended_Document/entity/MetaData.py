#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

from util.util import Base


class MetaData(Base):
    __tablename__ = "metadata"

    id = Column(Integer, ForeignKey('extended_document.id'), primary_key=True)
    title = Column(String)
    subject = Column(String)
    description = Column(String)
    refDate = Column(String)
    publicationDate = Column(String)
    type = Column(String)
    link = Column(String)
    originalName = Column(String)

    def __init__(self, title, subject, type, link):
        self.subject = subject
        self.title = title
        self.type = type
        self.link = link

    def update(self, newValues):
        for attKey, attVal in newValues.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)

    def getAllAttr(self):
        return {i for i in dir(self) if not (i.startswith('_') or callable(getattr(self, i)) or i == "metadata")}

    def serialize(self):
        objectSerialized = {}
        for attr in self.getAllAttr():
            objectSerialized[attr] = getattr(self, attr)
        return objectSerialized

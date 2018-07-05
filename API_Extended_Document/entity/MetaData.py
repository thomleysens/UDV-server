#!/usr/bin/env python3
# coding: utf8
import json

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from util.util import Base
from entity.ExtendedDocument import ExtendedDocument


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

    extendedDocument = relationship(ExtendedDocument, back_populates="metaData")

    def __init__(self, extended_document, title, subject, type, link):
        self.extendedDocument = extended_document
        self.subject = subject
        self.title = title
        self.type = type
        self.link = link

    def __str__(self):
        return "metaData: {id: " + str(self.id) + \
               "\ntitle: " + str(self.title) + \
               "\nsubject: " + str(self.subject) + \
               "\ndescription: " + str(self.description) + \
               "\nrefDate: " + str(self.refDate) + \
               "\npublicationDate: " + str(self.publicationDate) + \
               "\ntype: " + str(self.type) + \
               "\nlink: " + str(self.link) + \
               "\noriginalName: " + str(self.originalName)

    def update(self, newValues):
        for attKey, attVal in newValues.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)

    def serialise(self):
        return {"metaData": {"type": "metaData"}}

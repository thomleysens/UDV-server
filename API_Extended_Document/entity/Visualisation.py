#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from util.util import Base
from entity.ExtendedDocument import ExtendedDocument


class Visualisation(Base):
    __tablename__ = "visualisation"

    id = Column(Integer, ForeignKey('extended_document.id'), primary_key=True, )
    quaternionX = Column(Float)
    quaternionY = Column(Float)
    quaternionZ = Column(Float)
    quaternionW = Column(Float)
    positionX = Column(Float)
    positionY = Column(Float)
    positionZ = Column(Float)

    extendedDocument = relationship(ExtendedDocument, back_populates="visualisation")

    def __init__(self, extended_document):
        self.extendedDocument = extended_document

    def __str__(self):
        return "id: " + str(self.id) + \
               "\nquaternionX: " + str(self.quaternionX) + \
               "\nquaternionY: " + str(self.quaternionY) + \
               "\nquaternionZ: " + str(self.quaternionZ) + \
               "\nquaternionW: " + str(self.quaternionW) + \
               "\npositionX: " + str(self.positionX) + \
               "\npositionY: " + str(self.positionY) + \
               "\npositionZ: " + str(self.positionZ)

    def update(self, newValues):
        for attKey, attVal in newValues.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)

#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, Float
from sqlalchemy import ForeignKey

from util.db_config import Base
from entities.Entity import Entity


class Visualisation(Entity, Base):
    __tablename__ = "visualisation"

    id = Column(Integer, ForeignKey('document.id'),
                primary_key=True, )
    quaternionX = Column(Float)
    quaternionY = Column(Float)
    quaternionZ = Column(Float)
    quaternionW = Column(Float)
    positionX = Column(Float)
    positionY = Column(Float)
    positionZ = Column(Float)

#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import ForeignKey

from util.db_config import Base
from entities.Entity import Entity


class VersionDoc(Entity, Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer)
    user_id = Column(Integer,
                     ForeignKey("user.id"),
                     nullable=False)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(String, nullable=False)
    refDate = Column(DateTime(timezone=True))
    publicationDate = Column(DateTime(timezone=True))
    type = Column(String)
    file = Column(String)
    originalName = Column(String)
    quaternionX = Column(Float)
    quaternionY = Column(Float)
    quaternionZ = Column(Float)
    quaternionW = Column(Float)
    positionX = Column(Float)
    positionY = Column(Float)
    positionZ = Column(Float)
    version = Column(Integer, nullable=False)

#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

from util.db_config import Base
from entities.Entity import Entity


class MetaData(Entity, Base):
    __tablename__ = "metadata"

    id = Column(Integer, ForeignKey('extended_document.id'),
                primary_key=True)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(String, nullable=False)
    refDate = Column(String)
    publicationDate = Column(String)
    type = Column(String)
    file = Column(String)
    originalName = Column(String)

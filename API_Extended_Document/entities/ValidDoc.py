#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

from util.db_config import Base
from entities.Entity import Entity


class ValidDoc(Entity, Base):
    __tablename__ = "valid_doc"

    id_valid = Column(Integer, ForeignKey('extended_document.id'),
                primary_key=True)

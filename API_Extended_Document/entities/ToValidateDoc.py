#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

from util.db_config import Base
from entities.Entity import Entity


class ToValidateDoc(Entity, Base):
    __tablename__ = "to_validate_doc"

    id_to_validate = Column(Integer, ForeignKey('document.id'),
                            primary_key=True)


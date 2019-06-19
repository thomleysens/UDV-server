#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey

from util.db_config import Base
from entities.Entity import Entity


class Comment(Entity, Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    doc_id = Column(Integer, ForeignKey('document.id'))
    description = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)

#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from util.serialize import serialize
from util.db_config import Base

from entities.Entity import Entity


class DocumentUser(Base, Entity):
    __tablename__ = "document_user"

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, ForeignKey("document.id"))
    document = relationship("Document")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")

    def __init__(self, doc_id, user_id):
        self.doc_id = doc_id
        self.user_id = user_id

    def serialize(self):
        serialized_object = {}
        for attr in self.get_all_attr():
            if attr != 'document' and attr != 'user':
                serialized_object[attr] = serialize(getattr(self, attr))
        return serialized_object

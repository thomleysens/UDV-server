#!/usr/bin/env python3
# coding: utf8

import unicodedata

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from entities.Position import Position
from entities.ExtendedDocument import ExtendedDocument

from util.db_config import Base
from util.encryption import encrypt
from util.encryption import *
from util.serialize import serialize

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    position_id = Column(Integer, ForeignKey(Position.id))
    position = relationship(Position,
                            uselist=False)

    extended_document = relationship('ExtendedDocument',
                             cascade="all, delete-orphan")

    def update(self, new_values):
        for attKey, attVal in new_values.items():
            if hasattr(self, attKey):
                if(attVal):
                    setattr(self, attKey, attVal)
                else:
                    setattr(self, attKey, None)
        if 'password' in new_values:
            self.password = encrypt(new_values['password'])
        return self

    def set_position(self, position):
        self.position = position
        self.position_id = position.id

    def set_documents(self, documents):
        if(not(documents and is_valid_instances(documents))):
            return
        else:
            self.extended_document = documents.copy()

    @classmethod
    def get_attr(cls, attr_name):
        if hasattr(cls, attr_name):
            return getattr(cls, attr_name)
        return None

    def get_all_attr(self):
        return {i for i in dir(self)
                if not (i.startswith('_')
                        or callable(getattr(self, i))
                        or i == "metadata")}

    def is_valid_instance(self,obj):
        is_valid = True
        for attr in self.get_all_attr():
            if(not(attr in obj.keys() and position[str(attr)])):
                is_valid = False
                break
        return is_valid

    def is_valid_instances(self,objs):
        is_valid = True
        for obj in objs:
            if(not(is_valid_instance(obj))): 
                is_valid = False
                break
        return is_valid

    def serialize(self):
        serialized_object = {}
        for attr in self.get_all_attr():
            serialized_object[attr] = serialize(getattr(self, attr))
        return serialized_object

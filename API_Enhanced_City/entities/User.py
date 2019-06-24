#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from util.encryption import encrypt

from util.db_config import Base
from util.serialize import serialize
from util.Exception import UnprocessableEntity

from entities.Entity import Entity

from entities.UserRole import UserRole, LEVEL_MAX


class User(Entity, Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    role_id = Column(Integer, ForeignKey(UserRole.id))
    role = relationship(UserRole,
                        uselist=False)

    documentUser = relationship('DocumentUser',
                                cascade="all, delete-orphan")

    version = relationship('VersionDoc')

    comments = relationship("Comment",
                            cascade="all, delete-orphan")

    def update(self, new_values):
        for attKey, attVal in new_values.items():
            if hasattr(self, attKey):
                if attVal:
                    setattr(self, attKey, attVal)
                else:
                    setattr(self, attKey, None)
        if 'password' in new_values:
            self.password = encrypt(new_values['password'])
        return self

    def set_role(self, position):
        self.role = position
        self.role_id = position.id

    @staticmethod
    def is_admin(attributes):
        level = UserRole.get_clearance_level(attributes['role'])
        if level is None:
            raise UnprocessableEntity(f'Unknown role : {attributes["role"]}')
        return level == LEVEL_MAX

    def serialize(self):
        serialized_object = {}
        for attr in self.get_all_attr():
            if attr != 'password' and attr != 'comments' and attr != 'version' and attr != 'extended_document':
                serialized_object[attr] = serialize(getattr(self, attr))
        return serialized_object

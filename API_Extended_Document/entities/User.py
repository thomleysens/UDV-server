#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from util.encryption import encrypt

from util.db_config import Base
from entities.Entity import Entity

from entities.Position import Position


class User(Entity, Base):
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

    version = relationship('VersionDoc')

    comments = relationship("Comment",
                            uselist=False,
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

    def set_position(self, position):
        self.position = position
        self.position_id = position.id

    @staticmethod
    def is_admin(position):
        level = Position.get_clearance_level(position)
        return level == Position.LEVEL_MAX

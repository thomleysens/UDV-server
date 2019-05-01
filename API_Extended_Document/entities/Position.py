#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String

from util.db_config import Base
from util.serialize import serialize


class Position(Base):
    __tablename__ = "position"

    id = Column(Integer, primary_key=True)
    label = Column(String)

    clearance = ["contributor","softModerator","moderator","admin"]

    def __init__(self, label):
        self.label = label

    def update(self, new_values):
        for attKey, attVal in new_values.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)
        return self

    @staticmethod
    def getClearanceLevel(level):
        if(level == int(level) and 0 <= level < len(Position.clearance)):
            return Position.clearance[level]
        else:
            return Position.clearance[0]

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

    def serialize(self):
        serialized_object = {}
        for attr in self.get_all_attr():
            serialized_object[attr] = serialize(getattr(self, attr))
        return serialized_object

#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String

from util.db_config import Base
from entities.Entity import Entity


class Position(Entity, Base):
    __tablename__ = "position"

    id = Column(Integer, primary_key=True)
    label = Column(String)

    clearance = ["contributor", "softModerator", "moderator", "admin"]

    LEVEL_MIN = 1
    LEVEL_MAX = 3

    def __init__(self, label):
        self.label = label

    @staticmethod
    def get_clearance(level):
        if (level == int(level) and 0 <= level < len(
                Position.clearance)):
            return Position.clearance[level]
        else:
            return Position.clearance[0]

    @staticmethod
    def get_clearance_level(role):
        if role in Position.clearance:
            return Position.clearance.index(role)
        else:
            return None

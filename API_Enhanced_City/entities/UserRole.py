#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String

from util.db_config import Base
from entities.Entity import Entity

clearance = ["contributor", "softModerator", "moderator", "admin"]

LEVEL_MIN = 1
LEVEL_MAX = 3


class UserRole(Entity, Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True)
    label = Column(String)

    def __init__(self, label):
        self.label = label

    @staticmethod
    def get_clearance(level):
        if (level == int(level) and 0 <= level < len(
                clearance)):
            return clearance[level]
        else:
            return clearance[0]

    @staticmethod
    def get_clearance_level(role):
        if role in clearance:
            return clearance.index(role)
        else:
            return None

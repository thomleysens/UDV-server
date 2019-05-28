#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from util.db_config import Base
from entities.Entity import Entity

from entities.MetaData import MetaData
from entities.Visualisation import Visualisation
from entities.ValidDoc import ValidDoc
from entities.Position import Position
from entities.ToValidateDoc import ToValidateDoc


class ExtendedDocument(Entity, Base):
    __tablename__ = "extended_document"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer,
                     ForeignKey("user.id"),
                     nullable=False)

    metaData = relationship("MetaData",
                            uselist=False,
                            cascade="all, delete-orphan")

    comments = relationship("Comment",
                            cascade="all, delete-orphan")

    valid_doc = relationship("ValidDoc",
                             uselist=False,
                             cascade="all, delete-orphan")

    to_validate_doc = relationship("ToValidateDoc",
                                   uselist=False,
                                   cascade="all, delete-orphan")

    visualization = relationship("Visualisation",
                                 uselist=False,
                                 cascade="all, delete-orphan")

    def __init__(self, attributes):
        self.metaData = MetaData()
        self.visualization = Visualisation()
        if ExtendedDocument.is_allowed(attributes):
            self.valid_doc = ValidDoc()
        else:
            self.to_validate_doc = ToValidateDoc()

    def validate(self, attributes):
        self.valid_doc = ValidDoc()
        self.valid_doc.update(attributes)

    def update_initial(self, attributes):
        self.metaData.update(attributes)
        self.visualization.update(attributes)
        for attKey, attVal in attributes.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)
        if ExtendedDocument.is_allowed(attributes):
            self.valid_doc.update(attributes)
        else:
            self.to_validate_doc.update(attributes)

        return self

    def update(self, attributes):
        self.metaData.update(attributes)
        self.visualization.update(attributes)
        for attKey, attVal in attributes.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)
            if self.valid_doc:
                self.valid_doc.update(attributes)
            if self.to_validate_doc:
                self.to_validate_doc.update(attributes)
        return self

    @staticmethod
    def is_allowed(auth_info):
        role = auth_info['position']['label']
        level = Position.get_clearance_level(role)
        return level > Position.LEVEL_MIN

    def is_owner(self, auth_info):
        return auth_info['user_id'] == self.user_id

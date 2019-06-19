#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from util.serialize import serialize

from util.db_config import Base
from entities.Entity import Entity

from entities.Visualisation import Visualisation
from entities.Position import Position, LEVEL_MIN
from entities.ValidationStatus import ValidationStatus, Status


class Document(Entity, Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(String, nullable=False)
    refDate = Column(DateTime(timezone=True))
    publicationDate = Column(DateTime(timezone=True))
    type = Column(String)
    file = Column(String)
    originalName = Column(String)

    comments = relationship("Comment",
                            cascade="all, delete-orphan")

    validationStatus = relationship("ValidationStatus",
                                    uselist=False,
                                    cascade="all, delete-orphan")

    visualization = relationship("Visualisation",
                                 uselist=False,
                                 cascade="all, delete-orphan")

    documentUser = relationship('DocumentUser',
                                cascade="all, delete-orphan")

    def __init__(self, attributes):
        self.visualization = Visualisation()
        if Document.is_allowed(attributes):
            self.validationStatus = ValidationStatus(Status.Validated)
        else:
            self.validationStatus = ValidationStatus(Status.InValidation)

    def validate(self, attributes):
        self.validationStatus.validate()

    def update_initial(self, attributes):
        self.visualization.update(attributes)
        for attKey, attVal in attributes.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)

        return self

    def update(self, attributes):
        self.visualization.update(attributes)
        for attKey, attVal in attributes.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)
        return self

    @staticmethod
    def is_allowed(auth_info):
        role = auth_info['position']['label']
        level = Position.get_clearance_level(role)
        return level > LEVEL_MIN

    def owner_id(self):
        return self.documentUser[0].user_id

    def owner(self):
        return self.documentUser[0].user

    def is_owner(self, auth_info):
        return auth_info['user_id'] == self.owner_id()

    def serialize(self):
        serialized_object = {}
        for attr in self.get_all_attr():
            if attr != 'documentUser':
                serialized_object[attr] = serialize(getattr(self, attr))
        serialized_object['user_id'] = self.owner_id()
        return serialized_object

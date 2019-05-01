#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from entities.MetaData import MetaData
from entities.Visualisation import Visualisation
from entities.ValidDoc import ValidDoc
from entities.ToValidateDoc import ToValidateDoc
from util.db_config import Base
from util.serialize import serialize


class ExtendedDocument(Base):
    __tablename__ = "extended_document"

    id = Column(Integer, primary_key=True)
    metaData = relationship("MetaData",
                            uselist=False,
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
        if (attributes["validation"]):
            self.valid_doc = ValidDoc()
        else:
            self.to_validate_doc = ToValidateDoc()

    def validate(self, attributes):
            self.valid_doc = ValidDoc()
            self.valid_doc.update(attributes)

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

    def update(self, attributes):
        self.metaData.update(attributes)
        self.visualization.update(attributes)
        if (attributes["validation"]):
            self.valid_doc.update(attributes)
        else:
            self.to_validate_doc.update(attributes)

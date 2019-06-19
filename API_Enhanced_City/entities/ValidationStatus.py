#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, Enum
from sqlalchemy import ForeignKey

from util.db_config import Base
from entities.Entity import Entity

import enum


class Status(enum.Enum):
    Validated = enum.auto(),
    InValidation = enum.auto()


class ValidationStatus(Base, Entity):
    """
    Represents the validation status of a document. Statuses are represented by
    strings defined in the `ValidationStatus` file.
    """
    __tablename__ = "validation_status"

    doc_id = Column(Integer, ForeignKey('document.id'), primary_key=True)
    status = Column(Enum(Status), nullable=False)

    def __init__(self, status):
        """
        Creates a new Validation Status.
        :param Status status: The initial status of the document. Possible values are
        `Validated` and `InValidation`.
        """
        self.status = status

    def validate(self):
        """
        Changes the status of the document from `InValidation` to `Validated`.
        :return: None
        """
        if self.status == Status.InValidation:
            self.status = Status.Validated

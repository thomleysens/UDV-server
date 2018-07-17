#!/usr/bin/env python3
# coding: utf8

import persistence_unit.PersistenceUnit as pUnit
from util.db_config import *

from entities.ExtendedDocGuidedTour import ExtendedDocGuidedTour
from entities.GuidedTour import GuidedTour
from entities.ExtendedDocument import ExtendedDocument


class Controller:
    """
    Class that allows communication with the DB
    No instance is needed because all its methods are static.
    This methods are used to make a CRUD operation,
    by making a query or a transaction with the DB by using
    the decorators '~persistence_unit.PersistenceUnit.make_a_query'
    and make_a_transaction
    """

    @staticmethod
    def recreate_tables():
        Base.metadata.drop_all(pUnit.engine)
        Base.metadata.create_all(pUnit.engine)

    @staticmethod
    def create_tables():
        Base.metadata.create_all(pUnit.engine)

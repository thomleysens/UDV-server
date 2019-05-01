#!/usr/bin/env python3
# coding: utf8

import persistence_unit.PersistenceUnit as pUnit
from util.db_config import *
from entities.GuidedTour import GuidedTour
from entities.Position import Position
from entities.ExtendedDocument import ExtendedDocument
from entities.ExtendedDocGuidedTour import ExtendedDocGuidedTour
from entities.User import User


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
    @pUnit.make_a_transaction
    def create_position(session, label):
        position_exist = session.query(Position).filter(
            Position.label == label).scalar() is not None

        if not position_exist:
            position = Position(label)
            session.add(position)

    @staticmethod
    def recreate_tables():
        Base.metadata.drop_all(pUnit.engine)
        Controller.create_tables()

    @staticmethod
    def create_tables():
        Base.metadata.create_all(pUnit.engine)
        Controller.create_position("admin")
        Controller.create_position("moderator")
        Controller.create_position("softModerator")
        Controller.create_position("contributor")



#!/usr/bin/env python3
# coding: utf8

import persistence_unit.PersistenceUnit as pUnit
from util.db_config import *
from entities.GuidedTour import GuidedTour
from entities.Position import Position
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
    @pUnit.make_a_transaction
    def create_privileged_user(session, *args):
        attributes = args[0]
        user = User()
        user.set_position(session.query(Position).filter(
            Position.label == attributes["role"]).one())
        user.update(attributes)
        session.add(user)
        return user

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
        attributes = {"email": "gilles.gesquiere@insa-lyon.fr", "firstName": "Gilles", "lastName": "Gesquière",\
        "password": "MEPP2019", "role": "admin", "username": " admin_gilles"}
        Controller.create_privileged_user(attributes)

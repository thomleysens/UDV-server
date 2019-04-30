#!/usr/bin/env python3
# coding: utf8

from entities.Position import Position
import persistence_unit.PersistenceUnit as pUnit


class PositionController:
    """
    Class that allows communication with the DB
    No instance is needed because all its methods are static.
    This methods are used to make a CRUD operation,
    by making a query or a transaction with the DB by using
    the decorators '~persistence_unit.PersistenceUnit.make_a_query'
    and make_a_transaction
    """

    @staticmethod
    @pUnit.make_a_query
    def get_positions(session):
        return session.query(Position).all()

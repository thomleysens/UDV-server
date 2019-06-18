#!/usr/bin/env python3
# coding: utf8

from util.db_config import *
import persistence_unit.PersistenceUnit as pUnit
from controller.UserController import UserController
from controller.PositionController import PositionController

from entities.User import User
from entities.Position import Position
from entities.GuidedTour import GuidedTour
from entities.Document import Document
from entities.ExtendedDocGuidedTour import ExtendedDocGuidedTour
from entities.Comment import Comment
from entities.VersionDoc import VersionDoc


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
        Controller.create_tables()

    @staticmethod
    def create_tables():
        Base.metadata.create_all(pUnit.engine)
        PositionController.create_all_positions()
        UserController.create_admin()

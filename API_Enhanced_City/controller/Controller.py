#!/usr/bin/env python3
# coding: utf8

from util.db_config import *
import persistence_unit.PersistenceUnit as pUnit
from controller.UserController import UserController
from controller.UserRoleController import UserRoleController

from entities.User import User
from entities.UserRole import UserRole
from entities.GuidedTour import GuidedTour
from entities.Document import Document
from entities.DocumentGuidedTour import DocumentGuidedTour
from entities.Comment import Comment
from entities.VersionDoc import VersionDoc
from entities.DocumentUser import DocumentUser
from entities.ValidationStatus import ValidationStatus
from entities.Visualisation import Visualisation
from entities.LinkCityObject import LinkCityObject


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
        UserRoleController.create_all_roles()
        UserController.create_admin()

#!/usr/bin/env python3
# coding: utf8

from entities.UserRole import UserRole
import persistence_unit.PersistenceUnit as pUnit


class UserRoleController:
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
    def get_roles(session):
        return session.query(UserRole).all()

    @staticmethod
    @pUnit.make_a_transaction
    def create_role(session, label):
        position_exist = session.query(UserRole).filter(
            UserRole.label == label).scalar() is not None

        if not position_exist:
            position = UserRole(label)
            session.add(position)

    @staticmethod
    def create_all_roles():
        UserRoleController.create_role("admin")
        UserRoleController.create_role("moderator")
        UserRoleController.create_role("softModerator")
        UserRoleController.create_role("contributor")

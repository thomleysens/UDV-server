#!/usr/bin/env python3
# coding: utf8

import sqlalchemy.orm
from time import time
import jwt

from util.Exception import LoginError
from util.encryption import is_password_valid

from controller.Controller import Controller
import persistence_unit.PersistenceUnit as pUnit
from entities.User import User
from entities.Position import Position


class UserController:
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
    def create_user(session, *args):
        user = User()
        user.set_position(session.query(Position).filter(
            Position.label == Position.getClearanceLevel(0)).one())
        user.update(args[0])
        session.add(user)
        return user

    @staticmethod
    @pUnit.make_a_query
    def get_user_by_id(session, *args):
        user_id = args[0]
        return session.query(User).filter(
            User.id == user_id).one()

    @staticmethod
    @pUnit.make_a_transaction
    def login(session, *args):
        try:
            username = args[0]['username']
            password = args[0]['password']
            user = session.query(User).filter(
                User.username == username).one()
            if is_password_valid(user.password, password):
                exp = time() + 24 * 3600
                payload = {
                    'id': user.id,
                    'username': user.username,
                    'firstName': user.firstName,
                    'lastName': user.lastName,
                    'email': user.email,
                    'position': str(user.position.serialize()),
                    'exp': exp
                }
                return {
                    "token": jwt.encode(
                        payload, password, algorithm='HS256').decode(
                        'utf-8'
                    )
                }
        except sqlalchemy.orm.exc.NoResultFound:
            pass

        raise LoginError

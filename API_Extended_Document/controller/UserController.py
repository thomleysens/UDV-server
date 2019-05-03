#!/usr/bin/env python3
# coding: utf8

import sqlalchemy.orm
from time import time
import jwt

from util.Exception import LoginError
from util.encryption import *

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
        attributes = args[0]
        user = User()
        user.set_position(session.query(Position).filter(
            Position.label == Position.getClearance(0)).one())
        user.update(attributes)
        session.add(user)
        return user

    @staticmethod
    @pUnit.make_a_transaction
    def create_privileged_user(session, *args):
        attributes = args[0]
        admin = session.query(User).filter(User.id == attributes['user_id']).one()
        position = admin.position.label
        if(User.isAdmin(position)):
            user = User()
            user.set_position(session.query(Position).filter(
                Position.label == attributes["role"]).one())
            user.update(attributes)
            session.add(user)
            return user
        else:
            raise AuthError

    @staticmethod
    @pUnit.make_a_query
    def get_user_by_id(session, *args):
        attributes = args[0]
        user_id = attributes
        return session.query(User).filter(
            User.id == user_id).one()

    @staticmethod
    @pUnit.make_a_transaction
    def login(session, *args):
        try:
            attributes = args[0]
            username = attributes['username']
            password = attributes['password']
            user = session.query(User).filter(
                User.username == username).one()
            print(user.username) 
            if is_password_valid(user.password, password):
                exp = time() + 24 * 3600
                payload = {
                    'user_id'  : user.id,
                    'username' : user.username,
                    'firstName': user.firstName,
                    'lastName' : user.lastName,
                    'email'    : user.email,
                    'position' : str(user.position.serialize()),
                    'exp'      : exp
                }
                return {
                    "token": jwt.encode(payload, VarConfig.get()['password'], algorithm='HS256').decode('utf-8')
                }
        except sqlalchemy.orm.exc.NoResultFound:
            pass

        raise LoginError

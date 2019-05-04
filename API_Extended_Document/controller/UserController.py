#!/usr/bin/env python3
# coding: utf8

from time import time

from util.Exception import LoginError
from util.encryption import *

from entities.User import User
from entities.Position import Position
import persistence_unit.PersistenceUnit as pUnit


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
            Position.label == Position.get_clearance(0)).one())
        user.update(attributes)
        session.add(user)
        return user

    @staticmethod
    @pUnit.make_a_transaction
    def create_privileged_user(session, *args):
        attributes = args[0]
        position = attributes["user_position"]
        if User.is_admin(position):
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
            print(username)
            print(password)
            user = session.query(User).filter(
                User.username == username).one()
            print(user.username)
            print(user.password)
            if is_password_valid(user.password, password):
                print('valid')
                exp = time() + 24 * 3600
                payload = {
                    'user_id': user.id,
                    'username': user.username,
                    'firstName': user.firstName,
                    'lastName': user.lastName,
                    'email': user.email,
                    'position': str(user.position.serialize()),
                    'exp': exp
                }
                return {
                    "token": jwt.encode(
                        payload, VarConfig.get()['password'],
                        algorithm='HS256').decode('utf-8')
                }
            else:
                print('pas_valid')
                raise LoginError
        except Exception as e:
            print('Exception :')
            print(e)
            raise LoginError

    @staticmethod
    @pUnit.make_a_transaction
    def create_admin(session):
        print('try to create admin')
        user_exist = session.query(User).scalar() is not None
        if not user_exist:
            attributes = {
                "email": "gilles.gesquiere@insa-lyon.fr",
                "firstName": "Gilles",
                "lastName": "Gesquière",
                "password": "MEPP2019",
                "role": "admin",
                "username": "admin_gilles",
                "user_position": "admin"
            }
            UserController.create_privileged_user(attributes)

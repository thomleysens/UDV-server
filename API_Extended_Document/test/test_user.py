#!/usr/bin/env python3
# coding: utf8

from controller.Controller import Controller
from controller.UserController import UserController

from test.test_functions import *


class TestUser:
    nb_tests = 0
    nb_tests_succeed = 0

    # @TODO: create a method to check the success of uploading a file
    @staticmethod
    def create_user():
        print('\033[01m## Creation ##\033[0m')

        make_test(lambda: UserController.create_user({
            'username': 'John_Doe',
            'password': 'pwd',
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'John_Doe@mail.com'
        }))(UserTest, 'Normal Creation case', False)

        make_test(lambda: UserController.create_user({
            'username': '   ',
            'password': 'pwd',
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'John_Doe@mail.com'
        }))(UserTest, 'Empty username', True)

        make_test(lambda: UserController.create_user({
            'username': 'John_Doe1',
            'password': 'pwd',
            'firstName': 'John',
            'lastName': '',
            'email': 'John_Doe@mail.com1'
        }))(UserTest, 'Empty field', True)

        make_test(lambda: UserController.create_user({
            'username': 'John_Doe1',
            'password': 'pwd',
            'firstName': 'John',
            'email': 'John_Doe@mail.com1'
        }))(UserTest, 'Missing Field', True)

        make_test(lambda: UserController.create_user({
            'username': 'John_Doe12',
            'password': 'pwd',
            'firstName': 'John',
            'lastName':'Doe',
            'email': 'John_Doe@mail.com12',
            'fake:':'fake'
        }))(UserTest, 'Add Erronate Ignored Field', False)

        make_test(lambda: UserController.create_user({
            'username': 'John_Doe123',
            'password': 'pwd',
            'firstName': 'John',
            'lastName':'Doe',
            'lastName':'Doe1',
            'email': 'John_Doe@mail.com123',
        }))(UserTest, 'Add Duplicate Param Takes the last one', False)

        make_test(lambda: UserController.create_user({
            'username': 'John_Doe',
            'password': 'pwd',
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'John_Doe@mail.com1'
        }))(UserTest, 'Duplicate username', True)

        make_test(lambda: UserController.create_user({
            'username': 'John_Doe123',
            'password': 'pwd',
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'John_Doe@mail.com'
        }))(UserTest, 'Duplicate email', True)

        make_test(lambda: UserController.create_user({
            'username': 'John_Doe',
            'password': 'pwd',
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'John_Doe@mail.com'
        }))(UserTest, 'Duplicate username and email', True)

        make_test(lambda: UserController.create_user({
            'username': 'John_Doe1234',
            'lastName': 'Doe',
            'firstName': 'John',
            'password': 'pwd',
            'email': 'John_Doe1234@mail.com'
        }))(UserTest, 'Other normal case with unordered fields', False)

    @staticmethod
    def login():
        make_test(lambda: UserController.login({
            'username': 'John_Doe',
            'password': 'pwd'
        }))(UserTest, 'Login success', False)

        make_test(lambda: UserController.login({
            'password': 'pwd',
            'username': 'John_Doe'
        }))(UserTest, 'Login success with unordered fields', False)

        make_test(lambda: UserController.login({
            'username': 'John_Doe',
            'password': 'pwd1'
        }))(UserTest, 'Login with wrong pwd', True)

        make_test(lambda: UserController.login({
            'username': 'John_Doe',
            'password': ''
        }))(UserTest, 'Login with empty pwd', True)

        make_test(lambda: UserController.login({
            'username': 'John_Doe'
        }))(UserTest, 'Login with missing pwd', True)

        make_test(lambda: UserController.login({
            'username': 'John_Doe1',
            'password': 'pwd'
        }))(UserTest, 'Login with wrong username', True)

        make_test(lambda: UserController.login({
            'username': 'Jane',
            'password': 'pwd'
        }))(UserTest, 'Login with inexisting username', True)

        make_test(lambda: UserController.login({
            'username': '',
            'password': 'pwd'
        }))(UserTest, 'Login with empty username', True)

        make_test(lambda: UserController.login({
            'password': 'pwd'
        }))(UserTest, 'Login with missing username', True)

        make_test(lambda: UserController.login({
        }))(UserTest, 'Login with all missing fields', True)

        make_test(lambda: UserController.login({
        }))(UserTest, 'Login with all missing fields', True)

if __name__ == '__main__':
    Controller.recreate_tables()
    UserTest.create_user()
    UserTest.login()
    print('\n\n\033[04mSuccessTest\033[01m: ',
          UserTest.nb_tests_succeed, '/',
          UserTest.nb_tests, sep='')

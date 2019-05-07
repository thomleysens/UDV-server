#!/usr/bin/env python3
# coding: utf8

from controller.Controller import Controller
from controller.DocController import DocController
from controller.UserController import UserController

from test.user_tests import UserTest
from test.test_functions import *


class DocumentTest:
    nb_tests = 0
    nb_tests_succeed = 0

    # @TODO: create a method to check the success of uploading a file

    @staticmethod
    def create_documents():
        print('\033[01m## Creation ##\033[0m')

        make_test(lambda: UserController.create_user({
            'username': 'John_Doe',
            'password': 'pwd',
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'John_Doe@mail.com'
        }))(UserTest, 'Normal Creation case', False)

        make_test(lambda: UserController.create_user({
            'username': 'John_Doe1',
            'password': 'pwd',
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'John_Doe@mail.com1'
        }))(UserTest, 'Creation with rights case', False)

        make_test(lambda: DocController.create_document({
            'user_id': 1,
            'title': 'title',
            'subject': 'Subject1',
            'type': 'type',
            'description': 'a description',
            'link': '1.gif',
            'position': {'label': 'admin'}
        }))(DocumentTest, 'all needed attributes to validate', False)

        make_test(lambda: DocController.create_document({
            'user_id': 2,
            'title': 'title',
            'subject': 'Subject1',
            'type': 'type',
            'description': 'a description',
            'link': '1.gif',
            'position': {'label': 'contributor'}
        }))(
            DocumentTest, 'all needed attributes valid', False)

        make_test(lambda: DocController.create_document({
            'user_id': 2,
            'title': 'title',
            'subject': 'Subject2',
            'type': 'type',
            'description': 'a description',
            'link': '2.gif',
            'refDate': '2019-02-05',
            'position': {'label': 'admin'}
        }))(DocumentTest, 'all needed attributes to validate', False)

        make_test(lambda: DocController.create_document({
            'user_id': 2,
            'title': 'another title',
            'subject': 'Subject3',
            'type': 'type',
            'non_attr': 'non_value',
            'refDate': '2018-12-03',
            'description': 'an other description',
            'link': '3.png',
            'position': {'label': 'contributor'}
        }))(DocumentTest, 'needed + nonexistent attributes valid', False)

        make_test(lambda: DocController.create_document({
            'user_id': 2,
            'title': 'another title',
            'subject': 'Subject4',
            'type': 'type',
            'non_attr': 'non_value',
            'refDate': '2018-12-02',
            'description': 'an other description',
            'link': '4.png',
            'position': {'label': 'admin'}
        }))(DocumentTest, 'needed + nonexistent attributes to validate', False)

        make_test(lambda: DocController.create_document({
            'user_id': 2,
            'title': 'another title'
        }))(DocumentTest, 'needed argument missing', True)

        print('\033[01m## validation ##\033[0m')

        make_test(lambda: DocController.validate_document(2, {
            'user_id': 2,
            'position': {'label': 'contributor'}
        }))(DocumentTest, 'document validation by non admin', True)

        make_test(lambda: DocController.validate_document(2, {
            'user_id': 1,
            'position': {'label': 'admin'}
        }))(DocumentTest, 'document validation', False)

    @staticmethod
    def read_documents():
        print('\n\033[01m## Reading ##\033[0m')

        make_test(lambda: DocController.get_documents({}))(
            DocumentTest, 'all documents', False)

        make_test(lambda: DocController.get_documents({
            'keyword': 'description',
            'refDateStart': '2018-12-03'
        }))(DocumentTest, 'specific documents', False)

        make_test(lambda: DocController.get_documents_to_validate({
            'user_id': 3,
            'position': {'label': 'admin'}
        }))(DocumentTest, 'to validate documents', False)

        make_test(lambda: DocController.get_documents_to_validate({
            'user_id': 1,
            'position': {'label': 'contributor'}
        }))(DocumentTest, 'to validate documents non admin', False)

        make_test(lambda: DocController.get_document_by_id(1))(
            DocumentTest, 'document with existing id', False)

        make_test(lambda: DocController.get_document_by_id(-1))(
            DocumentTest, 'document with non existing id', True)

    @staticmethod
    def update_documents():
        print('\n\033[01m## Updating ##\033[0m')
        make_test(lambda: DocController.update_document(1, {
            'user_id': 2,
            'user_position': 'contributor',
            'positionX': 12,
            'description': 'description of a document',
            'position': {'label': 'contributor'}
        }))(DocumentTest, 'existing document to validate', True)

        make_test(lambda: DocController.update_document(2, {
            'user_id': 2,
            'user_position': 'admin',
            'positionX': 12,
            'description': 'another description',
            'position': {'label': 'admin'}
        }))(DocumentTest, 'existing document valid', False)

        make_test(lambda: DocController.update_document(-1, {
            'user_id': 2,
            'user_position': 'contributor',
            'positionX': 12,
            'description': 'description of a document'
        }))(DocumentTest, 'existing document to validate', True)

    @staticmethod
    def delete_documents():
        print('\n\033[01m## Deletion ##\033[0m')
        make_test(lambda: DocController.delete_documents(1, {
            'user_id': 2,
            'position': {'label': 'contributor'}
        }))(DocumentTest, 'delete existing document with unauthorized user', True)

        make_test(lambda: DocController.delete_documents(2, {
            'user_id': 3,
            'position': {'label': 'admin'}
        }))(DocumentTest, 'delete existing document with authorized user', False)


if __name__ == '__main__':
    Controller.recreate_tables()
    DocumentTest.create_documents()
    DocumentTest.read_documents()
    DocumentTest.update_documents()
    DocumentTest.delete_documents()
    print('\n\n\033[04mSuccess\033[01m: ',
          DocumentTest.nb_tests_succeed, '/',
          DocumentTest.nb_tests, sep='')

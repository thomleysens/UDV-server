#!/usr/bin/env python3
# coding: utf8

from controller.Controller import Controller
from controller.DocController import DocController

from test.test_functions import *


class DocumentTest:
    nb_tests = 0
    nb_tests_succeed = 0

    # @TODO: create a method to check the success of uploading a file

    @staticmethod
    def create_documents():
        print("\033[01m## Creation ##\033[0m")
        test_operation(DocumentTest, "all needed attributes",
                       False,
                       lambda: DocController.create_document(
                           {"title": "title",
                            "subject": "Subject1",
                            "type": "type",
                            "description": "a description",
                            "link": "1.gif"}))

        test_operation(DocumentTest, "all needed attributes",
                       False,
                       lambda: DocController.create_document(
                           {"title": "title",
                            "subject": "Subject2",
                            "type": "type",
                            "description": "a description",
                            "link": "2.gif",
                            "refDate": "2019-02-05"}))

        test_operation(DocumentTest, "needed + nonexistent attributes",
                       False,
                       lambda: DocController.create_document(
                           {"title": "another title",
                            "subject": "Subject3",
                            "type": "type",
                            "non_attr": "non_value",
                            "refDate": "2018-12-03",
                            "description": "an other description",
                            "link": "3.png"}))

        test_operation(DocumentTest, "needed argument missing",
                       True,
                       lambda: DocController.create_document(
                           {"title": "another title"}))

    @staticmethod
    def read_documents():
        print("\n\033[01m## Reading ##\033[0m")

        test_operation(DocumentTest, "all documents", False,
                       lambda: DocController.get_documents({}))

        test_operation(DocumentTest, "specific documents", False,
                       lambda: DocController.get_documents(
                           {"keyword": "description",
                            'refDateStart': '2018-12-03'}))

        test_operation(DocumentTest, "document with existing id", False,
                       lambda: DocController.get_document_by_id(1))

        test_operation(DocumentTest, "document with non existing id", True,
                       lambda: DocController.get_document_by_id(-1))

    @staticmethod
    def update_documents():
        print("\n\033[01m## Updating ##\033[0m")
        test_operation(DocumentTest, "existing document", False,
                       lambda: DocController.update_document(1, {
                           'positionX': 12,
                           'description': "description of a document"
                       }))

        test_operation(DocumentTest, "existing document", False,
                       lambda: DocController.update_document(1, {
                           'positionX': 12,
                           'description': "another description"
                       }))

        test_operation(DocumentTest, "existing document", True,
                       lambda: DocController.update_document(-1, {
                           'positionX': 12,
                           'description': "description of a document"
                       }))

    @staticmethod
    def delete_documents():
        print("\n\033[01m## Deletion ##\033[0m")
        test_operation(DocumentTest, "existing document", False,
                       lambda: DocController.delete_documents(2))
        test_operation(DocumentTest, "existing document", True,
                       lambda: DocController.delete_documents(2))


if __name__ == "__main__":
    Controller.recreate_tables()
    DocumentTest.create_documents()
    DocumentTest.read_documents()
    DocumentTest.update_documents()
    DocumentTest.read_documents()
    DocumentTest.delete_documents()
    DocumentTest.read_documents()
    print("\n\n\033[04mSuccess\033[01m: ", DocumentTest.nb_tests_succeed, "/",
          DocumentTest.nb_tests, sep="")

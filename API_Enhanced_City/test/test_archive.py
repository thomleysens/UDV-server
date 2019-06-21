#!/usr/bin/env python3
# coding: utf8
import pytest
import sqlalchemy.orm

from entities.ValidationStatus import Status
from controller.Controller import Controller
from controller.DocController import DocController
from controller.CommentController import CommentController
from controller.ArchiveController import ArchiveController


class TestArchive:

    def test_create_document(self):
        Controller.recreate_tables()
        print("Create a document")
        expected_response = {
            'id': 1,
            'comments': [],
            'user_id': 1,
            'publicationDate': None,
            'subject': 'Subject1',
            'title': 'title',
            'refDate': None,
            'file': '1.gif',
            'originalName': None,
            'description': 'a description',
            'type': 'type',
            'validationStatus': {
                'doc_id': 1,
                'status': Status.Validated
            }, 'visualization': {
                'quaternionZ': None,
                'positionZ': None,
                'positionX': None,
                'id': 1,
                'quaternionY': None,
                'quaternionW': None,
                'positionY': None,
                'quaternionX': None
            }
        }
        assert expected_response == DocController.create_document({
            'title': 'title',
            'subject': 'Subject1',
            'type': 'type',
            'description': 'a description',
            'file': '1.gif',
            'user_id': 1,
            "role": {
                'label' : 'admin'
            }
        }, {
            'user_id': 1
        })

    def test_update_document_1(self):
        print("update a document")
        expected_response = {
            'user_id': 1,
            'type': 'type',
            'publicationDate': None,
            'description': 'description of a document',
            'subject': 'Subject1',
            'file': '1.gif',
            'refDate': None,
            'title': 'title',
            'originalName': None,
            'id': 1,
            'visualization': {
                'quaternionY': None,
                'quaternionZ': None,
                'quaternionX': None,
                'id': 1,
                'positionY': None,
                'positionX': 12.0,
                'quaternionW': None,
                'positionZ': None
            },
            'validationStatus': {
                'status': Status.Validated,
                'doc_id': 1
            },
            'comments': [],
        }
        assert expected_response == DocController.update_document({
            'user_id': 1,
            "role": {
                'label': 'admin'
            }},
            1,
            {'positionX': 12,
             'description': 'description of a document'})

    def test_update_document_2(self):
        print("update a document")
        expected_response = {
            'user_id': 1,
            'refDate': None,
            'file': '1.gif',
            'publicationDate': None,
            'description': 'a new description',
            'originalName': None,
            'subject': 'Subject1',
            'type': 'type',
            'title': 'title',
            'visualization': {
                'positionZ': None,
                'quaternionX': None,
                'id': 1,
                'quaternionZ': None,
                'positionX': 12.0,
                'positionY': 15.0,
                'quaternionY': None,
                'quaternionW': None
            },
            'id': 1,
            'validationStatus': {
                'status': Status.Validated,
                'doc_id': 1
            },
            'comments': []
        }
        assert expected_response == DocController.update_document({
            'user_id': 1,
            'role': {
                'label': 'admin'
            }
        }, 1, {
            'positionY': 15,
            'description': 'a new description'
        })

    def test_delete_document(self):
        print("delete a document")
        expected_response = None
        assert expected_response == DocController.delete_documents(1, {
                'user_id' : 1,
                "role": {
                    'label' : 'admin'
                }
            })

    def test_get_archive(self):
        print("get the archives")
        expected_response =  [
            {
                'positionZ': None,
                'subject': 'Subject1',
                'quaternionW': None,
                'user_id': 1,
                'refDate': None,
                'id': 3,
                'positionX': 12.0,
                'quaternionX': None,
                'originalName': None,
                'version': 3,
                'quaternionY': None,
                'title': 'title',
                'description': 'a new description',
                'doc_id': 1,
                'file': '1.gif',
                'quaternionZ': None,
                'positionY': 15.0,
                'publicationDate': None,
                'type': 'type'
            },
            {
                'positionZ': None,
                'subject': 'Subject1',
                'quaternionW': None,
                'user_id': 1,
                'refDate': None,
                'id': 2,
                'positionX': 12.0,
                'quaternionX': None,
                'originalName': None,
                'version': 2,
                'quaternionY': None,
                'title': 'title',
                'description': 'description of a document',
                'doc_id': 1,
                'file': '1.gif',
                'quaternionZ': None,
                'positionY': None,
                'publicationDate': None,
                'type': 'type'
            },
            {
                'positionZ': None,
                'subject': 'Subject1',
                'quaternionW': None,
                'user_id': 1,
                'refDate': None,
                'id': 1,
                'positionX': None,
                'quaternionX': None,
                'originalName': None,
                'version': 1,
                'quaternionY': None,
                'title': 'title',
                'description': 'a description',
                'doc_id': 1,
                'file': '1.gif',
                'quaternionZ': None,
                'positionY': None,
                'publicationDate': None,
                'type': 'type'
            }
        ]
        assert expected_response == ArchiveController.get_archive(1)


if __name__ == "__main__":
    TestArchive().test_create_document()
    TestArchive().test_update_document_1()
    TestArchive().test_update_document_2()
    TestArchive().test_delete_document()
    TestArchive().test_get_archive()

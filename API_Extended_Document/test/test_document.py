#!/usr/bin/env python3
# coding: utf8

import pytest
import sqlalchemy.orm
import sqlalchemy.exc

from util.Exception import AuthError
from controller.Controller import Controller
from controller.DocController import DocController
from controller.UserController import UserController


class TestDocument:
    def test_document_init(self):
        Controller.recreate_tables()
        print("Starting document tests")

    def test_create_regular_user(self):
        print("Create a regular user")
        assert UserController.create_user({
            'username': 'John_Doe',
            'password': 'pwd',
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'John_Doe@mail.com'
        }) is not None

    def test_create_document_1(self):
        print('create document to validate with all needed attributes')
        expected_response = {
            'metaData': {
                'link': '1.gif',
                'description': 'a description',
                'subject': 'Subject1',
                'title': 'title',
                'originalName': None,
                'type': 'type',
                'publicationDate': None,
                'refDate': None, 'id': 1},
            'visualization': {
                'positionX': None,
                'quaternionY': None,
                'positionZ': None,
                'quaternionZ': None,
                'quaternionX': None,
                'id': 1,
                'positionY': None,
                'quaternionW': None
            },
            'user_id': 1,
            'valid_doc': {
                'id_valid': 1
            },
            'to_validate_doc': None,
            'comments': None,
            'id': 1}

        assert expected_response == DocController.create_document({
            'user_id': 1,
            'title': 'title',
            'subject': 'Subject1',
            'type': 'type',
            'description': 'a description',
            'link': '1.gif',
            'position': {'label': 'admin'}
        })

    def test_create_document_2(self):
        print('create extended document with all document with all '
              'needed attributes')
        expected_response = {
            'id': 2,
            'metaData': {
                'id': 2,
                'publicationDate': None,
                'refDate': '2019-02-05',
                'subject': 'Subject2',
                'link': '2.gif',
                'description': 'a description',
                'type': 'type',
                'originalName': None,
                'title': 'title'
            },
            'valid_doc': {
                'id_valid': 2
            },
            'user_id': 2,
            'comments': None,
            'to_validate_doc': None,
            'visualization': {
                'id': 2,
                'quaternionW': None,
                'positionZ': None,
                'quaternionZ': None,
                'positionX': None,
                'positionY': None,
                'quaternionY': None,
                'quaternionX': None
            }
        }
        assert expected_response == DocController.create_document({
            'user_id': 2,
            'title': 'title',
            'subject': 'Subject2',
            'type': 'type',
            'description': 'a description',
            'link': '2.gif',
            'refDate': '2019-02-05',
            'position': {'label': 'admin'}
        })

    def test_create_document_3(self):
        print('Create document with all needed and non existent '
              'attributes as a contributor')
        assert DocController.create_document({
            'user_id': 2,
            'title': 'another title',
            'subject': 'Subject3',
            'type': 'type',
            'non_attr': 'non_value',
            'refDate': '2018-12-02',
            'description': 'an other description',
            'link': '3.png',
            'position': {'label': 'contributor'}
        }) is not None

    def test_create_document_4(self):
        print('Create document with all needed and non existent '
              'attributes as an admin')
        assert DocController.create_document({
            'user_id': 1,
            'title': 'another title',
            'subject': 'Subject3',
            'type': 'type',
            'non_attr': 'non_value',
            'refDate': '2018-12-03',
            'description': 'details',
            'link': '3.png',
            'position': {'label': 'admin'}
        }) is not None

    def test_create_document_5(self):
        print('Create document with missing attributes')
        with pytest.raises(KeyError):
            DocController.create_document({
                'user_id': 2,
                'title': 'another title'
            })

    def test_validate_document_1(self):
        print('Validate a document as contributor')
        with pytest.raises(AuthError):
            DocController.validate_document(2, {
                'user_id': 2,
                'position': {'label': 'contributor'}
            })

    def test_validate_document_2(self):
        print('Validate a document as an admin')
        with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
            DocController.validate_document(2, {
                'user_id': 1,
                'position': {'label': 'admin'}
            })

    def test_get_all_documents(self):
        print('Get all documents')
        response = DocController.get_documents({})
        assert len(response) == 3
        assert response[0]['id'] == 1
        assert response[1]['id'] == 2
        assert response[2]['id'] == 4

    def test_get_specific_documents(self):
        print('Get specific documents')
        response = DocController.get_documents({
            'keyword': 'description',
            'refDateStart': '2018-12-03'
        })
        assert len(response) == 1
        assert response[0]['id'] == 2

    def test_get_documents_to_validate_admin(self):
        print('Get documents to validate as an admin')
        response = DocController.get_documents_to_validate({
            'user_id': 3,
            'position': {'label': 'admin'}
        })
        assert len(response) == 1
        assert response[0]['id'] == 3

    def test_get_documents_to_validate_contributor(self):
        print('Get documents to validate as a contributor')
        response = DocController.get_documents_to_validate({
            'user_id': 3,
            'position': {'label': 'admin'}
        })
        assert len(response) == 1
        assert response[0]['id'] == 3

    def test_get_document_by_id(self):
        print('Get a document by its id')
        assert 1 == DocController.get_document_by_id(1)['id']

    def test_get_non_existing_document(self):
        print('Get a document using a non existent id')
        with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
            DocController.get_document_by_id(-1)

    def test_update_document_as_contributor(self):
        print('Update a document as contributor')
        with pytest.raises(KeyError):
            DocController.update_document(1, {
                'user_id': 2,
                'user_position': 'contributor',
                'positionX': 12,
                'description': 'description of a document',
                'position': {'label': 'contributor'}
            })

    def test_update_document_as_admin(self):
        print('Update a document as admin')
        response = DocController.update_document(1, {
            'user_id': 2,
            'user_position': 'admin',
            'positionX': 12,
            'description': 'another description',
            'position': {'label': 'admin'}
        })
        assert response['visualization']['positionX'] == 12
        assert response['metaData']['description'] == \
               'another description'

    def test_update_non_existing_document(self):
        print('Update a non existing document')
        with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
            DocController.update_document(-1, {
                'user_position': 'admin',
                'positionX': 12,
                'description': 'another description',
                'user_id': 2,
                'position': {'label': 'admin'}
            })

    def test_delete_document_as_contributor(self):
        print('Delete a document as contributor')
        try:
            DocController.delete_documents(4, {
                'user_id': 2,
                'position': {'label': 'contributor'}
            })
        except (AuthError, sqlalchemy.orm.exc.NoResultFound):
            return

        pytest.fail('Error expected')

    # def test_delete_document_as_admin(self):
    #     print('Delete a document as admin')
    #     try:
    #         DocController.delete_documents(4, {
    #         'user_id': 1,
    #         'position': {'label': 'admin'}
    #     })
    #     except Exception as e:
    #         print(e)


if __name__ == "__main__":
    Controller.recreate_tables()
    TestDocument().test_create_regular_user()
    a = DocController.create_document({
        'user_id': 1,
        'title': 'title',
        'subject': 'Subject1',
        'type': 'type',
        'description': 'a description',
        'link': '1.gif',
        'position': {'label': 'admin'}
    })
    print(a)

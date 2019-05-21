#!/usr/bin/env python3
# coding: utf8

import pytest
import sqlalchemy.orm
import sqlalchemy.exc

from controller.Controller import Controller
from controller.DocController import DocController
from controller.TourController import TourController


class TestGuidedTour:
    def test_create_tours_1(self):
        Controller.recreate_tables()
        print("all needed attributes")
        expected_response = {
            'extendedDocs': [],
            'name': 'First tour',
            'id': 1,
            'description': 'This is the first guided tour'
        }
        assert expected_response == TourController.create_tour(
            "First tour", "This is the first guided tour")

    def test_create_tours_2(self):
        print("all needed attributes")
        expected_response = {
            'extendedDocs': [],
            'name': 'Second tour',
            'id': 2,
            'description': 'This is the second guided tour'
        }
        assert expected_response == TourController.create_tour(
            "Second tour", "This is the second guided tour")

    def test_create_tours_3(self):
        print("all needed attributes")
        expected_response = {
            'extendedDocs': [],
            'name': 'Third tour',
            'id': 3,
            'description': 'This is the third guided tour'
        }
        assert expected_response == TourController.create_tour(
            "Third tour", "This is the third guided tour")

    def test_create_tours_4(self):
        print("needed argument missing")
        with pytest.raises(IndexError):
            TourController.create_tour()

    def test_read_tours_1(self):
        print("all tours")
        expected_response = 3
        assert expected_response == len(TourController.get_tours())

    def test_read_tours_2(self):
        print("tour with existing id")
        expected_response = {
            'extendedDocs': [],
            'name': 'First tour',
            'id': 1,
            'description': 'This is the first guided tour'
        }
        assert expected_response == TourController.get_tour_by_id(1)

    def test_read_tours_3(self):
        print("tour with non existing id")
        with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
            TourController.get_tour_by_id(-1)

    def test_update_tour_1(self):
        DocController.create_document({
            "title": "title",
            "subject": "Subject1",
            "type": "type",
            "description": "a description",
            "link": "1.gif",
            'user_id': 1,
            'position': {'label': 'admin'}
        })
        DocController.create_document({
            "title": "title2",
            "subject": "Subject2",
            "type": "type",
            "description": "a description",
            "link": "1.gif",
            'user_id': 1,
            'position': {'label': 'admin'}
        })
        print("adding existing document")
        expected_response = {
            'extendedDocs': [{
                'id': 1,
                'title': None,
                'tour_id': 1,
                'doc_position': 1,
                'text2': None,
                'doc_id': 1,
                'document': {
                    'id': 1,
                    'valid_doc': {
                        'id_valid': 1
                    },
                    'user_id': 1,
                    'comments': [],
                    'to_validate_doc': None,
                    'metaData': {
                        'id': 1,
                        'title': 'title',
                        'type': 'type',
                        'publicationDate': None,
                        'link': '1.gif',
                        'description': 'a description',
                        'subject': 'Subject1',
                        'originalName': None,
                        'refDate': None},
                    'visualization': {
                        'positionZ': None,
                        'id': 1,
                        'quaternionW': None,
                        'positionY': None,
                        'quaternionZ': None,
                        'quaternionX': None,
                        'positionX': None,
                        'quaternionY': None}},
                'text1': None}],
            'name': 'First tour',
            'id': 1,
            'description': 'This is the first guided tour'
        }
        assert expected_response == TourController.add_document(1, 1)

    def test_update_tour_2(self):
        print("adding twice existing document")
        expected_response = {
            'extendedDocs': [{
                'id': 1,
                'title': None,
                'tour_id': 1,
                'doc_position': 1,
                'text2': None,
                'doc_id': 1,
                'document': {
                    'id': 1,
                    'comments': [],
                    'valid_doc': {
                        'id_valid': 1
                    },
                    'user_id': 1,
                    'to_validate_doc': None,
                    'metaData':
                        {'id': 1,
                         'title': 'title',
                         'type': 'type',
                         'publicationDate': None,
                         'link': '1.gif',
                         'description': 'a description',
                         'subject': 'Subject1',
                         'originalName': None,
                         'refDate': None},
                    'visualization': {
                        'positionZ': None,
                        'id': 1,
                        'quaternionW': None,
                        'positionY': None,
                        'quaternionZ': None,
                        'quaternionX': None,
                        'positionX': None,
                        'quaternionY': None
                    },
                },
                'text1': None},
                {
                    'id': 2,
                    'title': None,
                    'tour_id': 1,
                    'doc_position': 2,
                    'text2': None,
                    'doc_id': 1,
                    'document': {
                        'id': 1,
                        'comments': [],
                        'valid_doc': {
                            'id_valid': 1
                        },
                        'user_id': 1,
                        'to_validate_doc': None,
                        'metaData': {
                            'id': 1,
                            'title': 'title',
                            'type': 'type',
                            'publicationDate': None,
                            'link': '1.gif',
                            'description': 'a description',
                            'subject': 'Subject1',
                            'originalName': None,
                            'refDate': None},
                        'visualization': {
                            'positionZ': None,
                            'id': 1,
                            'quaternionW': None,
                            'positionY': None,
                            'quaternionZ': None,
                            'quaternionX': None,
                            'positionX': None,
                            'quaternionY': None
                        }
                    },
                    'text1': None}
            ],
            'name': 'First tour',
            'id': 1,
            'description': 'This is the first guided tour'
        }
        assert expected_response == TourController.add_document(1, 1)

    def test_update_tour_3(self):
        print("adding non existing document")
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            TourController.add_document(1, 3)

    def test_update_tour_4(self):
        print("updating existing guided tour")
        response = TourController.update(1, {
            'description': 'new description'
        })
        assert response['description'] == 'new description'

    def test_delete_tour_1(self):
        print("existing tour")
        assert TourController.delete_tour(3) is None

    def test_delete_tour_2(self):
        print("non existing tour")
        with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
            TourController.delete_tour(3)


if __name__ == "__main__":
    Controller.recreate_tables()
    TestGuidedTour().test_update_tour_1()

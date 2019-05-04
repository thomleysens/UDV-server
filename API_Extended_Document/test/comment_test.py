#!/usr/bin/env python3
# coding: utf8
import pytest
import sqlalchemy.orm

from controller.Controller import Controller
from controller.DocController import DocController
from controller.CommentController import CommentController


class TestComment:

    def test_create_document(self):
        Controller.recreate_tables()
        print("Create a valid document")
        expected_response = {
            'id': 1,
            'comments': None,
            'user_id': 1,
            'metaData': {
                'publicationDate': None,
                'subject': 'Subject1',
                'id': 1,
                'title': 'title',
                'refDate': None,
                'link': '1.gif',
                'originalName': None,
                'description': 'a description',
                'type': 'type'
            }, 'valid_doc': {
                'id_valid': 1
            }, 'visualization': {
                'quaternionZ': None,
                'positionZ': None,
                'positionX': None,
                'id': 1,
                'quaternionY': None,
                'quaternionW': None,
                'positionY': None,
                'quaternionX': None
            }, 'to_validate_doc': None
        }
        assert expected_response == DocController.create_document({
            'title': 'title',
            'subject': 'Subject1',
            'type': 'type',
            'description': 'a description',
            'link': '1.gif',
            'user_id' : 1,
            "user_position": "admin"
        })

    def test_create_comment_1(self):
        print("Create a comment")
        expected_response = {
            'doc_id': 1,
            'id': 1,
            'user_id': 1,
            'description': 'ok'
        }
        assert expected_response == CommentController.create_comment({
            'doc_id' : 1,
            'user_id' : 1,
            'description' : 'ok'
        })

    def test_create_comment_2(self):
        print("Create a comment")
        expected_response = {
            'doc_id': 1,
            'id': 2,
            'user_id': 1,
            'description': 'ok_2'
        }
        assert expected_response == CommentController.create_comment({
            'doc_id' : 1,
            'user_id' : 1,
            'description' : 'ok_2'
        })

    def test_update_comment(self):
        print("update a comment")
        expected_response = {
            'doc_id': 1,
            'user_id': 1,
            'description': 'ok_1',
            'id': 1
        }
        assert expected_response == CommentController.update_comment(1, {
            'id' : 1,
            'user_id' : 1,
            "user_position": "admin",
            'description' : 'ok_1'
        })

    def test_delete_comment(self):
        print("delete a comment")
        expected_response = None
        assert expected_response == CommentController.delete_comment(2, {
            'user_id' : 1,
            "user_position": "admin"
        })

    def test_get_comments(self):
        print("get comments")
        expected_response = [
            {
                'id': 1,
                'description': 'ok_1',
                'doc_id': 1,
                'user_id': 1
            }
        ]
        assert expected_response == CommentController.get_comments(1)

if __name__ == "__main__":
    TestComment().test_create_document()
    TestComment().test_create_comment_1()
    TestComment().test_create_comment_2()
    TestComment().test_update_comment()
    TestComment().test_delete_comment()
    TestComment().test_get_comments()

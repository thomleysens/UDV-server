#!/usr/bin/env python3
# coding: utf8
import sys

from controller.Controller import Controller


def create_documents():
    Controller.create_document(
        {"title": "titre", "subject": "subject1", "type": "type",
         "link": "link", "description": "une description"})
    Controller.create_document(
        {"title": "another titre", "subject": "subject", "type": "type",
         "link": "link", "description": "une autre description"})


def read_documents():
    print(Controller.serialize(Controller.get_documents(
        {"title": "titre", "subject": "subject1"})))
    print(Controller.serialize(Controller.get_document_by_id(1)))
    print(Controller.serialize(Controller.get_document_by_id(2)))


def update_documents():
    Controller.update_document(1, {
        'positionX': 12,
        'description': "this is a very boring description of a very "
                       "boring document"
    })

    Controller.update_document(2, {
        'positionX': 12,
        'description': "this is a very boring description of a very "
                       "boring document"
    })

    Controller.update_document(3, {
        'positionX': 12,
        'description': "this is a very boring description of a very "
                       "boring document"
    })


def delete_documents():
    Controller.delete_documents(1)
    Controller.delete_documents(1)


if __name__ == "__main__":
    Controller.recreate_tables()
    create_documents()
    read_documents()
    update_documents()
    delete_documents()
    read_documents()

#!/usr/bin/env python3
# coding: utf8
from contextlib import contextmanager

from colorama import Fore
from colorama import Style

from controller.Controller import Controller
from util.log import info_logger


def create_documents():
    print("\033[01m## Creation ##\033[0m")
    with make_atomic_transaction("all needed attributes"):
        Controller.create_document(
            {"title": "title", "subject": "subject1", "type": "type",
             "link": "link", "description": "a description"})

    with make_atomic_transaction(
            "all needed attributes + non existing attributes"):

        Controller.create_document(
            {"title": "another title", "subject": "subject",
             "type": "type", "non_attr": "non_value",
             "refDate": "2018-12-03",
             "link": "link", "description": "an other description"})

    with make_atomic_transaction("needed argument missing"):
        Controller.create_document({"title": "another title"})

    print("")


def read_documents():
    print("\033[01m## Reading ##\033[0m")

    docs = None
    with make_atomic_transaction("all documents"):
        docs = Controller.serialize(Controller.get_documents({}))
    print(f"\t\t\t{Fore.BLUE}", docs, sep="")

    with make_atomic_transaction("specific documents"):
        docs = Controller.serialize(Controller.get_documents(
            {"title": "titre", 'refDateStart': '2018-12-03'}))
    print(f"\t\t\t{Fore.BLUE}", docs, sep="")

    doc = None
    with make_atomic_transaction("document with existing id"):
        doc = Controller.serialize(Controller.get_document_by_id(1))
    print(f"\t\t\t{Fore.BLUE}", doc, sep="")

    with make_atomic_transaction("document with non existing id"):
        doc = Controller.serialize(Controller.get_document_by_id(3))
    print(f"\t\t\t{Fore.BLUE}", doc, sep="")
    print("")


def update_documents():
    print("\033[01m## Updating ##\033[0m")
    with make_atomic_transaction("existing document"):
        Controller.update_document(1, {
            'positionX': 12,
            'description': "description of a very boring document"
        })

    with make_atomic_transaction("existing document"):
        Controller.update_document(2, {
            'positionX': 12,
            'description': "description of a very boring document"
        })

    with make_atomic_transaction("non existing document"):
        Controller.update_document(3, {
            'positionX': 12,
            'description': "description of a very boring document"
        })
    print('')


def delete_documents():
    print("\033[01m## Deletion ##\033[0m")
    with make_atomic_transaction("existing document"):
        Controller.delete_documents(1)
    with make_atomic_transaction("non existing document"):
        Controller.delete_documents(1)
    print('')


@contextmanager
def make_atomic_transaction(description=""):
    try:
        yield
        print(f"{Fore.GREEN}[success]{Style.RESET_ALL}", end=' ')
        print('\t', description, '\033[0m', sep='')
    except Exception as e:
        print(f"{Fore.RED}[ error ]{Style.RESET_ALL}", end=' ')
        print('\t', description, sep='', end=':')
        print(f"{Fore.RED}", str(e).replace("\n", ""),
              f"{Style.RESET_ALL}")


if __name__ == "__main__":
    Controller.recreate_tables()
    create_documents()
    read_documents()
    update_documents()
    read_documents()
    delete_documents()
    read_documents()

#!/usr/bin/env python3
# coding: utf8
import sys
from json import dumps

from sqlalchemy import or_, and_

from controller.Controller import Controller
from entity.DocumentTour import DocumentTour
from util.log import *
from util.db_config import *

from controller.DocController import DocController

from entity.ExtendedDocument import ExtendedDocument
from entity.GuidedTour import GuidedTour

import persistence_unit.PersistenceUnit as pUnit
from util.serialize import serialize


class TourController:
    """
    Class that allows communication with the DB
    No instance is needed because all its methods are static.
    This methods are used to make a CRUD operation,
    by making a query or a transaction with the DB by using
    the decorators '~persistence_unit.PersistenceUnit.make_a_query'
    and make_a_transaction
    """
    keyword_attr = ["title", "description"]

    @staticmethod
    @pUnit.make_a_transaction
    def create_tour(session, *args):
        name = args[0]
        description = args[1]
        document = GuidedTour(name, description)
        session.add(document)
        return document

    @staticmethod
    @pUnit.make_a_query
    def get_tour_by_id(session, *args):
        doc_id = args[0]
        return session.query(GuidedTour).filter(
            GuidedTour.id == doc_id).one()

    @staticmethod
    @pUnit.make_a_transaction
    def get_tour_by_keyword(session, *args):
        session.query(GuidedTour).all()

    @staticmethod
    @pUnit.make_a_transaction
    def add_document(session, *args):
        tour_id = args[0]
        doc_id = args[1]

        document = session.query(ExtendedDocument).filter(
            ExtendedDocument.id == doc_id).one()
        guided_tour = session.query(GuidedTour).filter(
            GuidedTour.id == tour_id).one()

        guided_tour.extendedDocs.append(document)
        session.add(guided_tour)

    @staticmethod
    @pUnit.make_a_transaction
    def remove_document(session, *args):
        tour_id = args[0]
        doc_id = args[1]

        document = session.query(ExtendedDocument).filter(
            ExtendedDocument.id == doc_id).one()
        guided_tour = session.query(GuidedTour).filter(
            GuidedTour.id == tour_id).one()

        guided_tour.extendedDocs.remove(document)
        session.add(guided_tour)

    @staticmethod
    @pUnit.make_a_transaction
    def delete_tour(session, *args):
        an_id = args[0]
        a_tour = session.query(GuidedTour).filter(
            GuidedTour.id == an_id).one()
        session.delete(a_tour)


if __name__ == "__main__":
    sys.stdout = open('../file.json', 'w')
    Controller.recreate_tables()
    TourController.create_tour("second", "second guided tour ever make")

    print(dumps(TourController.get_tour_by_id(1)))
    # TourController.add_document(1, 3)"""
    # TourController.remove_document(1, 1)

#!/usr/bin/env python3
# coding: utf8

from util.Exception import *

from sqlalchemy import func

import persistence_unit.PersistenceUnit as pUnit
from entities.GuidedTour import GuidedTour
from entities.DocumentGuidedTour import DocumentGuidedTour


class TourController:
    """
    Class that allows communication with the DB
    No instance is needed because all its methods are static.
    This methods are used to make a CRUD operation,
    by making a query or a transaction with the DB by using
    the decorators 'make_a_query' and 'make_a_transaction' from
    'persistence_unit.PersistenceUnit'
    """
    keyword_attr = ["title", "description"]

    @staticmethod
    @pUnit.make_a_transaction
    def create_tour(session, *args):
        name = args[0]
        description = args[1]
        guided_tour = GuidedTour(name, description)
        session.add(guided_tour)
        return guided_tour

    @staticmethod
    @pUnit.make_a_query
    def get_tour_by_id(session, *args):
        tour_id = args[0]
        return session.query(GuidedTour).filter(
            GuidedTour.id == tour_id).one()

    @staticmethod
    @pUnit.make_a_transaction
    def get_tours(session, *args):
        # @TODO: research like for ExtendedDoc could be set up
        return session.query(GuidedTour).all()

    @staticmethod
    @pUnit.make_a_transaction
    def add_document(session, *args):
        tour_id = args[0]
        doc_id = args[1]

        query_result = session.query(
            func.max(DocumentGuidedTour.doc_position).label(
                "doc_number")).filter(
            DocumentGuidedTour.tour_id == tour_id).one()

        doc_number = query_result.doc_number
        if not doc_number:
            doc_number = 0

        session.add(
            DocumentGuidedTour(tour_id, doc_id, doc_number + 1))

        return session.query(GuidedTour).filter(
            GuidedTour.id == tour_id).one()

    @staticmethod
    @pUnit.make_a_transaction
    def update(session, *args):
        tour_id = args[0]
        attributes = args[1]

        guided_tour = session.query(GuidedTour) \
            .filter(GuidedTour.id == tour_id).one()
        guided_tour.update(attributes)
        session.add(guided_tour)

        return guided_tour

    @staticmethod
    @pUnit.make_a_transaction
    def update_document(session, *args):
        tour_id = args[0]
        doc_id = args[1]
        attributes = args[2]

        guided_tour = session.query(GuidedTour) \
            .filter(GuidedTour.id == tour_id).one()
        guided_tour.update_document(doc_id, attributes)
        session.add(guided_tour)

        return guided_tour

    @staticmethod
    @pUnit.make_a_transaction
    def remove_document(session, tour_id, doc_position):
        guided_tour = session.query(GuidedTour).filter(
            GuidedTour.id == tour_id).one()
        doc_position -= 1

        try:
            guided_tour.extendedDocs.pop(doc_position)
        except Exception:
            raise NotFound("Document is not in Guided Tour")
        session.add(guided_tour)
        return guided_tour

    @staticmethod
    @pUnit.make_a_transaction
    def delete_tour(session, *args):
        an_id = args[0]
        a_tour = session.query(GuidedTour).filter(
            GuidedTour.id == an_id).one()
        session.delete(a_tour)
        return a_tour

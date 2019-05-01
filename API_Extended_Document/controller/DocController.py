#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import or_, and_

from entities.ExtendedDocGuidedTour import ExtendedDocGuidedTour
from util.log import *
from util.upload import UPLOAD_FOLDER
from util.db_config import *
from entities.MetaData import MetaData
from entities.ExtendedDocument import ExtendedDocument
from entities.ToValidateDoc import ToValidateDoc
import persistence_unit.PersistenceUnit as pUnit


class DocController:
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
    def create_document(session, *args):
        attributes = args[0]
        document = ExtendedDocument(attributes)
        document.update(attributes)
        session.add(document)
        return document

    @staticmethod
    @pUnit.make_a_transaction
    def validate_document(session, *args):
        attributes = args[0]
        id = attributes["id"]
        document = session.query(ExtendedDocument).filter(
            ExtendedDocument.id == id).one()
        to_validate = session.query(ToValidateDoc).filter(
            ToValidateDoc.id_to_validate == id).one()
        document.validate(attributes)
        session.delete(to_validate)
        session.add(document)
        return document

    @staticmethod
    @pUnit.make_a_query
    def get_document_by_id(session, *args):
        doc_id = args[0]
        return session.query(ExtendedDocument).filter(
            ExtendedDocument.id == doc_id).one()

    @staticmethod
    @pUnit.make_a_query
    def get_documents(session, *args):
        """
        This method si used to make a research using three criteria :
         - keyword research, document with attributes containing keyword
         - comparison research, search between two dates
         - attribute research, document with specific attributes values
        :param session: Session object
        :param args: List<attributes>
        :return: List<ExtendedDocument>
        """

        # @TODO: delete strong dependence to MetaData
        # list that will contain research conditions for the query
        keyword_conditions = []
        attributes = args[0]

        if attributes.get("keyword"):
            keyword = attributes.pop("keyword")
            for attr in DocController.keyword_attr:
                keyword_conditions.append(
                    MetaData.get_attr(attr).ilike('%' + keyword + '%'))

        comparison_conditions = []
        # dictionaries of attributes to compare
        inf_dict = {key.replace('Start', ''): attributes[key]
                    for key in attributes if 'Start' in key}
        sup_dict = {key.replace('End', ''): attributes[key]
                    for key in attributes if 'End' in key}

        # remove dictionaries to compare
        attributes = {key: attributes[key] for key in attributes
                      if not ('Start' in key or 'End' in key)}

        for attr in sup_dict.keys():
            comparison_conditions.append(
                MetaData.get_attr(attr) <= sup_dict[attr])

        for attr in inf_dict.keys():
            comparison_conditions.append(
                MetaData.get_attr(attr) >= inf_dict[attr])

        query = session.query(ExtendedDocument).join(
            MetaData).filter_by(**attributes).filter(
            and_(*comparison_conditions)).filter(
            or_(*keyword_conditions))

        return query.all()

    @staticmethod
    @pUnit.make_a_transaction
    def update_document(session, *args):
        doc_id = args[0]
        attributes = args[1]

        document = session.query(ExtendedDocument) \
            .filter(ExtendedDocument.id == doc_id).one()
        document.update(attributes)
        session.add(document)

        return document

    @staticmethod
    @pUnit.make_a_transaction
    def delete_documents(session, *args):
        an_id = args[0]
        a_doc = session.query(ExtendedDocument).filter(
            ExtendedDocument.id == an_id).one()
        # we also remove the associated image located in 'UPLOAD_FOLDER' directory
        os.remove(UPLOAD_FOLDER + '/' + a_doc.metaData.link)
        session.delete(a_doc)

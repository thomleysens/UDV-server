#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import or_, and_

from entities.ExtendedDocGuidedTour import ExtendedDocGuidedTour
from util.log import *
from util.upload import UPLOAD_FOLDER
from util.Exception import *
from util.db_config import *
from entities.MetaData import MetaData
from entities.User import User
from entities.ExtendedDocument import ExtendedDocument
from entities.ToValidateDoc import ToValidateDoc
from entities.ValidDoc import ValidDoc
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
        user = session.query(User).filter(User.id == attributes['user_id']).one()
        attributes['position'] = user.position.label
        document = ExtendedDocument(attributes)
        document.update_initial(attributes)
        session.add(document)
        return document

    @staticmethod
    @pUnit.make_a_transaction
    def validate_document(session, *args):
        attributes = args[0]
        id = attributes["id"]
        user = session.query(User).filter(User.id == attributes['user_id']).one()
        attributes['position'] = user.position.label
        if(ExtendedDocument.isAllowed(attributes)):
            document = session.query(ExtendedDocument).filter(
                ExtendedDocument.id == id).one()
            to_validate = session.query(ToValidateDoc).filter(
                ToValidateDoc.id_to_validate == id).one()
            document.validate(attributes)
            session.delete(to_validate)
            session.add(document)
            return document
        else:
            raise AuthError

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
            or_(*keyword_conditions)).join(ValidDoc)

        return query.all()

    @staticmethod
    @pUnit.make_a_query
    def get_documents_to_validate(session, *args):
        """
        This method si used to get documents to validate
        """
        attributes = args[0]
        user = session.query(User).filter(User.id == attributes['user_id']).one()
        attributes['position'] = user.position.label
        if(ExtendedDocument.isAllowed(attributes)):
            query = session.query(ExtendedDocument).join(ToValidateDoc)
            return query.all()
        else:
            query = session.query(ExtendedDocument).join(ToValidateDoc).join(session.query(User).filter(User.id == attributes['user_id']).one())
            return query.all()

    @staticmethod
    @pUnit.make_a_transaction
    def update_document(session, *args):
        doc_id = args[0]
        attributes = args[1]
        user = session.query(User).filter(User.id == attributes['user_id']).one()
        attributes['position'] = user.position.label
        document = session.query(ExtendedDocument) \
            .filter(ExtendedDocument.id == doc_id).one()
        #To change not supposed to be done in Controller
        if(ExtendedDocument.isAllowed(attributes)):
            document.update(attributes)
            session.add(document)
            return document
        else:
            raise AuthError

    @staticmethod
    @pUnit.make_a_transaction
    def delete_documents(session, *args):
        an_id = args[0]
        attributes = args[1]
        user = session.query(User).filter(User.id == attributes['user_id']).one()
        attributes['position'] = user.position.label
        #To change not supposed to be done in Controller
        if(ExtendedDocument.isAllowed(attributes)):
            # we also remove the associated image located in 'UPLOAD_FOLDER' directory
            a_doc = session.query(ExtendedDocument).filter(
                ExtendedDocument.id == an_id).one()
            os.remove(UPLOAD_FOLDER + '/' + a_doc.metaData.link)
            session.delete(a_doc)
        else:
            a_doc = session.query(ExtendedDocument).filter(
                ExtendedDocument.id == an_id).one().join(session.query(User).filter(User.id == attributes['user_id']).one())
            os.remove(UPLOAD_FOLDER + '/' + a_doc.metaData.link)
            session.delete(a_doc)

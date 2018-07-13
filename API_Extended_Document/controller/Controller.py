#!/usr/bin/env python3
# coding: utf8
import copy

from sqlalchemy import or_, and_

from util.log import *
from util.db_config import *
from entity.MetaData import MetaData
from entity.ExtendedDocument import ExtendedDocument
import persistence_unit.PersistenceUnit as pUnit


class Controller:
    keyword_attr = ["title", "description"]

    @staticmethod
    def recreate_tables():
        Base.metadata.drop_all(pUnit.engine)
        Base.metadata.create_all(pUnit.engine)

    @staticmethod
    @pUnit.make_a_transaction
    def create_document(session, *args):
        attributes = args[0]
        document = ExtendedDocument()
        document.update(attributes)
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
        # @TODO: delete strong dependence to MetaData

        # list that will contain research conditions for the query
        keyword_conditions = []
        attributes = args[0]

        if attributes.get("keyword"):
            keyword = attributes.pop("keyword")
            for attr in Controller.keyword_attr:
                keyword_conditions.append(
                    MetaData.get_attr(attr).ilike(
                        '%' + keyword + '%'))

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
    @pUnit.make_a_query
    def get_documents_by_keyword(session, *args):
        keyword = args[0]

        # @TODO: delete strong dependence to MetaData
        query = session.query(ExtendedDocument).join(MetaData)
        filter_condition = []
        for attr in Controller.keyword_attr:
            filter_condition.append(MetaData.get_attr(attr).ilike(
                '%' + keyword + '%'))
        return query.filter(or_(*filter_condition)).all()

    @staticmethod
    @pUnit.make_a_transaction
    def update_document(session, *args):
        doc_id = args[0]
        attributes = args[1]

        document = session.query(ExtendedDocument) \
            .filter(ExtendedDocument.id == doc_id).one()
        document.update(attributes)
        session.add(document)

    @staticmethod
    @pUnit.make_a_transaction
    def delete_documents(session, *args):
        an_id = args[0]
        a_doc = session.query(ExtendedDocument).filter(
            ExtendedDocument.id == an_id).one()
        session.delete(a_doc)

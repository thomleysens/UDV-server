#!/usr/bin/env python3
# coding: utf8
from sqlalchemy import or_, and_

from util.log import *
from util.db_config import *
from entity.MetaData import MetaData
from entity.ExtendedDocument import ExtendedDocument
import persistence_unit.PersistenceUnit as pUnit


class NullException(object):
    pass


class Controller:
    keyword_attr = ["title", "description"]

    @staticmethod
    def recreate_tables():
        Base.metadata.drop_all(pUnit.engine)
        Base.metadata.create_all(pUnit.engine)

    @staticmethod
    def create_document(attributes):
        with pUnit.make_a_transaction() as session:
            document = ExtendedDocument()
            document.update(attributes)
            session.add(document)

    @staticmethod
    def get_document_by_id(doc_id):
        with pUnit.make_a_query() as session:
            return session.query(ExtendedDocument).filter(
                ExtendedDocument.id == doc_id).one()

    @staticmethod
    def get_documents(attributes):
        with pUnit.make_a_query() as session:
            # dictionaries of attributes to compare
            sup_dict = {key.replace('<', ''): attributes[key]
                        for key in attributes if '<' in key}
            inf_dict = {key.replace('>', ''): attributes[key]
                        for key in attributes if '>' in key}

            # remove dictionaries to compare
            attributes = {key: attributes[key] for key in attributes
                          if not ('<' in key or '>' in key)}

            filter_condition = []
            for attr in sup_dict.keys():
                filter_condition.append(
                    MetaData.get_attr(attr) <= sup_dict[attr])

            for attr in inf_dict.keys():
                filter_condition.append(
                    MetaData.get_attr(attr) >= inf_dict[attr])

            documents = session.query(ExtendedDocument).join(
                MetaData).filter(and_(*filter_condition)).filter_by(
                **attributes)

            return documents.all()

    @staticmethod
    def get_documents_by_keyword(keyword):
        # @TODO: delete strong dependence to MetaData
        with pUnit.make_a_query() as session:
            query = session.query(ExtendedDocument).join(MetaData)
            filter_condition = []
            for attr in Controller.keyword_attr:
                filter_condition.append(MetaData.get_attr(attr).ilike(
                    '%' + keyword + '%'))
            return query.filter(or_(*filter_condition)).all()

    @staticmethod
    def update_document(doc_id, attributes):
        with pUnit.make_a_transaction() as session:
            document = session.query(ExtendedDocument) \
                .filter(ExtendedDocument.id == doc_id).one()
            document.update(attributes)
            session.add(document)

    @staticmethod
    def delete_documents(an_id):
        with pUnit.make_a_transaction() as session:
            a_doc = session.query(ExtendedDocument).filter(
                ExtendedDocument.id == an_id).one()
            session.delete(a_doc)

    @staticmethod
    def serialize(document):
        if type(document) is list:
            doc_lists = []
            for doc in document:
                doc_lists.append(doc.serialize())
            return doc_lists
        elif type(document) is ExtendedDocument:
            return document.serialize()
        else:
            raise NullException

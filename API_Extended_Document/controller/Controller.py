#!/usr/bin/env python3
# coding: utf8

from util.log import *
from util.db_config import *
from entity.MetaData import MetaData
from entity.ExtendedDocument import ExtendedDocument
import persistence_unit.PersistenceUnit as pUnit


class Controller:
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
        # @FIXME: impossible to manipulate 'metadata' and
        # 'visualisation' if session is closed
        with pUnit.make_a_query() as session:
            return session.query(ExtendedDocument).join(
                MetaData).filter_by(**attributes).all()

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
            return None

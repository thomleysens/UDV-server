#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import desc

from util.log import *
from entities.VersionDoc import VersionDoc
import persistence_unit.PersistenceUnit as pUnit


class ArchiveController:
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
    def create_archive(session, *args):
        attributes = args[0]['metaData']
        attributes.update(args[0]['visualization'])
        attributes['user_id'] = args[0]['user_id']
        attributes['doc_id'] = args[0]['id']
        del attributes['id']
        last = None
        try:
            last = session.query(VersionDoc).filter(
                VersionDoc.doc_id == attributes['doc_id']).order_by(
                desc(VersionDoc.version)).first()
        except Exception as e:
            print(e)
            info_logger.error(e)
        if last:
            attributes['version'] = last.serialize()['version'] + 1
        else:
            attributes['version'] = 1
        archive = VersionDoc()
        archive.update(attributes)
        session.add(archive)
        return archive

    @staticmethod
    @pUnit.make_a_query
    def get_archive(session, *args):
        """
        This method si used get all the archives of a document
        """
        doc_id = args[0]
        query = session.query(VersionDoc).filter(
            VersionDoc.doc_id == doc_id).order_by(
            desc(VersionDoc.version))

        return query.all()

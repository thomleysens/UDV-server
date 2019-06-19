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

    @staticmethod
    @pUnit.make_a_transaction
    def create_archive(session, *args):
        attributes = ArchiveController.remake_attribute(args[0])
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
        This method is used get all the archives of a document
        """
        doc_id = args[0]
        query = session.query(VersionDoc).filter(
            VersionDoc.doc_id == doc_id).order_by(
            desc(VersionDoc.version))

        return query.all()

    #@TODO refactor versionDoc in order to take 2 attributes metadata & visualisation instead of attribute in one table
    @staticmethod
    def remake_attribute(attributes):
        new_attributes = attributes
        new_attributes.update(attributes['visualization'])
        new_attributes['user_id'] = attributes['user_id']
        new_attributes['doc_id'] = attributes['id']
        del new_attributes['id']
        return new_attributes


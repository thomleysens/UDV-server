#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import or_, and_

from util.log import *
from util.upload import UPLOAD_FOLDER
from util.Exception import *

from entities.Comment import Comment
from entities.User import User
from entities.ExtendedDocument import ExtendedDocument

import persistence_unit.PersistenceUnit as pUnit


class CommentController:
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
    def create_comment(session, *args):
        attributes = args[0]
        comment = Comment()
        comment.update(attributes)
        session.add(comment)
        return comment

    @staticmethod
    @pUnit.make_a_query
    def get_comments(session, *args):
        """
        This method si used to make a research the comments of a document
        """
        attributes = args[0]

        query = session.query(Comment).filter(
            and_(Comment.doc_id == attributes["doc_id"]))

        return query.all()

    @staticmethod
    @pUnit.make_a_transaction
    def update_comment(session, *args):
        comment_id = args[0]
        attributes = args[1]
        params = {'description' : attributes['description']}
        comment = session.query(Comment) \
            .filter(Comment.id == comment_id).one()
        # To change not supposed to be done in Controller
        if (ExtendedDocument.is_allowed(attributes) or comment.user_id == attributes['user_id']):
            comment.update(params)
            session.add(comment)
            return comment
        else:
            raise AuthError

    @staticmethod
    @pUnit.make_a_transaction
    def delete_comment(session, *args):
        an_id = args[0]
        attributes = args[1]
        # To change not supposed to be done in Controller
        if ExtendedDocument.is_allowed(attributes):
            # we also remove the associated image
            # located in 'UPLOAD_FOLDER' directory
            comment = session.query(Comment).filter(
                Comment.id == an_id).one()
            session.delete(comment)
        else:
            comment = session.query(Comment).filter(and_(
                Comment.id == an_id,
                Comment.user_id == attributes[
                    'user_id'])).one()
            session.delete(comment)

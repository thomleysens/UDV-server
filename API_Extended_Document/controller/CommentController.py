#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import or_, and_

from util.log import *
from util.upload import UPLOAD_FOLDER
from util.Exception import *

from entities.Comment import Comment
from entities.User import User
from entities.Document import Document

import persistence_unit.PersistenceUnit as pUnit

import datetime


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
        doc_id = args[0]
        attributes = args[1]
        attributes['doc_id'] = doc_id
        attributes['date'] = datetime.datetime.utcnow().astimezone()
        comment = Comment()
        comment.update(attributes)
        session.add(comment)
        return comment

    @staticmethod
    @pUnit.make_a_query
    def get_comment(session, comment_id):
        """
        This method is used to fetch a comment by its id
        :param session: The SQLAlchemy session
        :param comment_id: The ID of the comment
        :return: The comment with the specified ID
        """
        comment = session.query(Comment).filter(Comment.id == comment_id).one()
        return comment

    @staticmethod
    @pUnit.make_a_query
    def get_comments(session, *args):
        """
        This method is used to make a research the comments of a document
        """
        doc_id = args[0]

        query = session.query(Comment).filter(
            and_(Comment.doc_id == doc_id)).order_by(Comment.date.desc())

        return query.all()

    @staticmethod
    @pUnit.make_a_transaction
    def update_comment(session, *args):
        comment_id = args[0]
        attributes = args[1]
        comment = session.query(Comment).filter(Comment.id == comment_id).one()
        if Document.is_allowed(attributes) or comment.user_id == attributes['user_id']:
            comment.update(attributes)
            session.add(comment)
            return comment
        else:
            raise AuthError

    @staticmethod
    @pUnit.make_a_transaction
    def delete_comment(session, *args):
        an_id = args[0]
        attributes = args[1]
        comment = session.query(Comment).filter(Comment.id == an_id).one()
        if Document.is_allowed(attributes) or comment.user_id == attributes['user_id']:
            session.delete(comment)
            return comment
        else:
            raise AuthError


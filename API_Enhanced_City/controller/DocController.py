#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import or_, and_

from util.log import *
from util.upload import *
from util.Exception import *

from entities.Document import Document
from entities.ValidationStatus import ValidationStatus, Status
from entities.DocumentUser import DocumentUser
from controller.ArchiveController import ArchiveController

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
    def create_document(session, attributes, auth_info):
        document = Document(attributes)
        document.update_initial(attributes)
        session.add(document)
        # Commit to assign an id to the document
        session.commit()
        document_user = DocumentUser(document.id, auth_info['user_id'])
        session.add(document_user)
        return document

    @staticmethod
    @pUnit.make_a_transaction
    def validate_document(session, *args):
        doc_id = args[0]
        attributes = args[1]
        if Document.is_allowed(attributes):
            document = session.query(Document).filter(
                Document.id == doc_id).one()
            document.validate(attributes)
            session.add(document)
            return document
        else:
            raise AuthError

    @staticmethod
    @pUnit.make_a_query
    def get_document_by_id(session, doc_id, auth_info):
        """
        Gets a document by its id. The code is a bit tricky because in the case
        where the document is in validation, only an admin or the owner of the
        document can access it.
        :param session: The SQLAlchemy session
        :param doc_id: An id of a document
        :param auth_info: The auth info
        :return: The extended document with the correct id
        :raises AuthError: if this is a document in validation and the user has
        no privilege on it
        :raises NoResultFound: if the document isn't in the database
        """
        # If we're an admin, no need to check what document it is
        if auth_info is None or not Document.is_allowed(auth_info):
            document = session.query(Document).join(ValidationStatus) \
                              .filter(Document.id == doc_id).one()
            # If the document is validated, everybody can see it
            if document.validationStatus.status != Status.Validated:
                # The only case where we're not allowed to access the document
                # is when it's in validation and we're neither the owner nor an
                # admin
                if auth_info is None:
                    # In this case we return unauthorized because the user could
                    # access the resource if he/she authenticate
                    raise Unauthorized
                if document.owner_id() != auth_info["user_id"]:
                    # In this case we return forbidden because the user is
                    # authenticated but hasn't the rights on the doc
                    raise AuthError
        return session.query(Document).filter(
            Document.id == doc_id).one()

    @staticmethod
    def get_document_file_location(doc_id, auth_info):
        document = DocController.get_document_by_id(doc_id, auth_info)
        filename = document['file']
        location = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(location):
            return location
        raise NotFound("File doest not exist")

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
                    Document.get_attr(attr).ilike('%' + keyword + '%'))

        comparison_conditions = [ValidationStatus.status == Status.Validated]

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
                Document.get_attr(attr) <= sup_dict[attr])

        for attr in inf_dict.keys():
            comparison_conditions.append(
                Document.get_attr(attr) >= inf_dict[attr])

        query = session.query(Document).join(ValidationStatus).filter_by(
            **attributes).filter(
            and_(*comparison_conditions)).filter(
            or_(*keyword_conditions))

        return query.all()

    @staticmethod
    @pUnit.make_a_query
    def get_documents_to_validate(session, *args):
        """
        This method si used to get documents to validate
        """
        attributes = args[0]
        if Document.is_allowed(attributes):
            query = session.query(Document).join(ValidationStatus).filter(
                ValidationStatus.status == Status.InValidation)
            return query.all()
        else:
            documents = session.query(Document).join(ValidationStatus).filter(
                ValidationStatus.status == Status.InValidation).all()
            return [doc for doc in documents if doc.owner_id() == attributes['user_id']]

    @staticmethod
    @pUnit.make_a_transaction
    def update_document(session, auth_info, doc_id, attributes):
        document = session.query(Document) \
            .filter(Document.id == doc_id).one()
        # To change not supposed to be done in Controller
        documents = session.query(Document).join(ValidationStatus).filter(
            and_(Document.id == doc_id,
                 ValidationStatus.status == Status.InValidation)).all()
        doc_count = len([doc for doc in documents
                         if doc.owner_id() == auth_info['user_id']])
        if Document.is_allowed(auth_info) or doc_count > 0:
            ArchiveController.create_archive(document.serialize())
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
        documents = session.query(Document).filter(
            Document.id == an_id).all()
        doc_count = len([doc for doc in documents
                         if doc.owner_id() == attributes['user_id']])
        if Document.is_allowed(attributes) or doc_count > 0:
            # we also remove the associated image
            # located in 'UPLOAD_FOLDER' directory
            a_doc = session.query(Document).filter(
                Document.id == an_id).one()
            if a_doc:
                ArchiveController.create_archive(a_doc.serialize())
                session.delete(a_doc)
            try:
                os.remove(UPLOAD_FOLDER + '/' + a_doc.file)
                return a_doc
            except Exception as e:
                print(e)
                info_logger.error(e)
        else:
            raise AuthError

    @staticmethod
    @pUnit.make_a_transaction
    def delete_document_file(session, auth_info, doc_id):
        document = session.query(Document) \
            .filter(Document.id == doc_id).one()
        if document:
            if document.is_owner(auth_info) or \
               Document.is_allowed(auth_info):
                filename = document.file
                if filename:
                    ArchiveController.create_archive(document.serialize())
                    document.update({
                        'file': None
                    })
                    session.add(document)
                    return document
                else:
                    raise NotFound
            else:
                raise AuthError
        else:
            raise NotFound

    @staticmethod
    @pUnit.make_a_query
    def check_authorization(session, auth_info, doc_id):
        """
        Checks if the authenticated user has rights on the document identified
        by the `doc_ic`. The function returns `True` only if the user is the
        owner of the document or an admin
        :param session: The sqlalchemy session
        :param auth_info: The authenticated use info
        :param doc_id: The document id
        :return: True if the user has rights on the document, False otherwise
        """
        document = session.query(Document) \
            .filter(Document.id == doc_id).one()
        return Document.is_allowed(auth_info) \
               or document.is_owner(auth_info)

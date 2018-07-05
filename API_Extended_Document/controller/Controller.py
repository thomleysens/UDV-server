#!/usr/bin/env python3
# coding: utf8

import sys

from util.log import *
from util.util import *
from entity.MetaData import MetaData
from entity.Visualisation import Visualisation
from entity.ExtendedDocument import ExtendedDocument
import persistenceUnit.PersistenceUnit as pUnit


class Controller:
    @staticmethod
    def createDocument(extended_document, metaData, visualisation):
        with pUnit.makeATransaction() as session:
            session.add(extended_document)
            session.add(metaData)
            session.add(visualisation)

    @staticmethod
    def recreateTables():
        Base.metadata.drop_all(pUnit.engine)
        Base.metadata.create_all(pUnit.engine)

    @staticmethod
    def getAllDocuments():
        with pUnit.makeATransaction() as session:
            return session.query(ExtendedDocument)

    @staticmethod
    def getDocumentById(anId):
        # @FIXME: impossible to manipulate 'metadata' and 'visualisation' if session is closed
        with pUnit.makeAQuery() as session:
            return session.query(ExtendedDocument).filter(ExtendedDocument.id == anId).one()

    @staticmethod
    def getDocuments(attributes):
        # @FIXME: impossible to manipulate 'metadata' and 'visualisation' if session is closed
        with pUnit.makeAQuery() as session:
            return session.query(ExtendedDocument).join(MetaData).filter_by(**attributes).all()

    """
    dictionary 'attributes' must contain a key id
    """

    @staticmethod
    def updateDocument(attributes):
        with pUnit.makeATransaction() as session:
            aDoc = session.query(ExtendedDocument).filter(ExtendedDocument.id == attributes['id']).one()
            aDoc.update(attributes)
            session.add(aDoc)
            session.add(aDoc.metaData)
            session.add(aDoc.visualisation)

    @staticmethod
    def deleteDocuments(anId):
        with pUnit.makeATransaction() as session:
            aDoc = session.query(ExtendedDocument).filter(ExtendedDocument.id == anId).one()
            session.delete(aDoc)


if __name__ == "__main__":
    # sys.stdout = open('result.log', 'w')

    Controller.recreateTables()

    doc = ExtendedDocument()
    meta = MetaData(doc, "un titre", "un sujet", "un type", "un link")
    visual = Visualisation(doc)
    Controller.createDocument(doc, meta, visual)

    doc = ExtendedDocument()
    meta = MetaData(doc, "un autre titre", "un sujet", "un type", "un link")
    visual = Visualisation(doc)
    Controller.createDocument(doc, meta, visual)

    Controller.updateDocument(
        {'id': 1, 'positionX': 12, 'description': "this is a very boring description of a very boring document"})
    Controller.deleteDocuments(2)

    print(Controller.getDocumentById(1))

    for i in Controller.getDocuments({'subject': 'un sujet'}):
        print("\n##\n", i, "\n##\n")
        print(i.serialize())

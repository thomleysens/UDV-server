#!/usr/bin/env python3
# coding: utf8

from entity.ExtendedDocument import ExtendedDocument


def serialize(document):
    if type(document) is list:
        doc_lists = []
        for doc in document:
            doc_lists.append(doc.serialize())
        return doc_lists
    elif type(document) is ExtendedDocument:
        return document.serialize()

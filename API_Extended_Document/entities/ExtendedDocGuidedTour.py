#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Table, Text, Column, ForeignKey, Integer

from util.db_config import Base

DocumentTour = Table('document_tour', Base.metadata,
                     Column('doc_id',
                            ForeignKey('extended_document.id'),
                            primary_key=True),
                     Column('tour_id',
                            ForeignKey('guided_tour.id'),
                            primary_key=True))

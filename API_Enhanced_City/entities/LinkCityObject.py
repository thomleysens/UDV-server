#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey

from util.db_config import Base
from entities.Entity import Entity


class LinkCityObject(Base, Entity):
    """
    Represents a link between a document and a city object.
    """
    __tablename__ = "link_city_object"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('document.id'), nullable=False)
    target_id = Column(String, nullable=False)
    centroid_x = Column(Float)
    centroid_y = Column(Float)
    centroid_z = Column(Float)

    def __init__(self, source_id, target_id, centroid_x, centroid_y, centroid_z):
        """
        Creates a link between a document and a city object.

        :param int source_id: ID of the source document.
        :param str target_id: ID of the target city object.
        """
        self.source_id = source_id
        self.target_id = target_id
        self.centroid_x = centroid_x
        self.centroid_y = centroid_y
        self.centroid_z = centroid_z
        # @todo Check if target_id corresponds to a existing city object

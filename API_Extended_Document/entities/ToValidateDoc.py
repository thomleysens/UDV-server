#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

from util.db_config import Base


class ToValidateDoc(Base):
    __tablename__ = "to_validate_doc"

    id_to_validate = Column(Integer, ForeignKey('extended_document.id'),
                            primary_key=True)

    def update(self, new_values):
        for attKey, attVal in new_values.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)
        return self

    @classmethod
    def get_attr(cls, attr_name):
        if hasattr(cls, attr_name):
            return getattr(cls, attr_name)
        return None

    def get_all_attr(self):
        return {i for i in dir(self)
                if not (i.startswith('_')
                        or callable(getattr(self, i))
                        or i == "metadata")}

    def serialize(self):
        serialized_object = {}
        for attr in self.get_all_attr():
            serialized_object[attr] = getattr(self, attr)
        return serialized_object

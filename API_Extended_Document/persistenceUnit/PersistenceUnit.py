#!/usr/bin/env python3
# coding: utf8

import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from util.util import get_db_info

db_string = get_db_info("config.yml")
engine = create_engine(db_string)
Session = sessionmaker(engine)


"""
makeATransaction is a function that allows to re-use the same code
The function is split into two parts : everything below the keyword 'yield' and everything below
The first part of the code is first executed and return the variable after 'yield' 
(in this case 'session').
The one that calls the contextmanager executes then its code and can have access to the return variable
Finally the second part of the contextmanager is executed whatever happens   
"""


@contextmanager
def makeATransaction():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()


@contextmanager
def makeAQuery():
    session = Session()
    try:
        yield session
    except Exception as e:
        print(e)

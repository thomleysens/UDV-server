#!/usr/bin/env python3
# coding: utf8

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from util.db_config import get_db_info

db_string = get_db_info("util/config.yml")
engine = create_engine(db_string)
Session = sessionmaker(engine)

"""
makeATransaction is a function that allows to re-use the same code
The function is split into two parts : 
everything below the keyword 'yield' and everything below
The first part of the code is first executed and return the variable 
after 'yield' (in this case 'session').
The one that calls the contextmanager executes then its code and can 
have access to the return variable
Finally the second part of the contextmanager is executed in all cases   
"""


@contextmanager
def make_a_transaction():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


@contextmanager
def make_a_query():
    session = Session()
    yield session

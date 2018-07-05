#!/usr/bin/env python3
# coding: utf8

import yaml
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
default_db_info = 'postgresql://postgres:password@localhost:5432/extendedDoc'


def get_db_info(config_file_name):
    try:
        with open(config_file_name, 'r') as file:
            config = yaml.load(file)

        db_info = \
            config['ordbms'] + "://" + \
            config["user"] + ":" + \
            config["password"] + "@" + \
            config["host"] + ":" + \
            str(config["port"]) + "/" + \
            config["dbname"]

        return db_info

    except (FileNotFoundError, KeyError):
        return default_db_info

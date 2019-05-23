#!/usr/bin/env python3
# coding: utf8

import os
import re
from flask import safe_join

import uuid

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def get_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()


def allowed_file(extension):
    return extension in ALLOWED_EXTENSIONS


def save_file(file):
    if not os.path.isdir(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    extension = get_extension(file.filename)
    if extension in ALLOWED_EXTENSIONS:
        filename = f'{str(uuid.uuid4())}.{extension}'
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename
    else:
        return None


def delete_file(filename):
    os.remove(os.path.join(filename))


def find_image(member_id):
    pattern = fr'^{member_id}\.[a-z]+$'
    rex = re.compile(pattern)
    files = os.listdir(
        safe_join(os.getcwd(), UPLOAD_FOLDER))
    for file in files:
        if rex.search(file):
            return file

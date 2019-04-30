#!/usr/bin/env python3
# coding: utf8

import json
import hmac
import base64
import hashlib
import random
import string
import jwt

from passlib.hash import pbkdf2_sha256

from util.Exception import AuthError
from util.VarConfig import VarConfig


def create_password():
    return ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for i in range(15))


def encrypt(password):
    return pbkdf2_sha256.encrypt(password)


def is_password_valid(hash_password, password):
    return pbkdf2_sha256.verify(password, hash_password)


def encode_base64(string):
    string = base64.b64encode(bytes(string, 'utf-8')).decode('utf-8')
    return string.translate(str.maketrans({
        '+': '-', '/': '_', '=': ''
    }))


def decode_base64(string):
    string += len(string) % 4 * '='
    return base64.b64decode(string).decode('utf-8')


if __name__ == '__main__':
    encoded_JWT = jwt.encode({
        'id': 1,
        'username': 'cool'
    }, VarConfig.get()['password'], algorithm='HS256')
    decoded_JWT = jwt.decode(encoded_JWT, VarConfig.get()['password'], algorithms=['HS256'])
    print(encoded_JWT)
    print(decoded_JWT)


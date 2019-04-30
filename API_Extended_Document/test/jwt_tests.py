#!/usr/bin/env python3
# coding: utf8

import jwt

from test.test_functions import *

class JwtTest:
    nb_tests = 0
    nb_tests_succeed = 0

    def encodeDocument():
        print('\033[01m## Creation ##\033[0m')
        #
        make_test(lambda: jwt.encode({
        'id': 1,
        'username': 'cool'}, 'password', algorithm='HS256'))(JwtTest, 'Encode message', False)

    def decodeDocument():
        print('\033[01m## Creation ##\033[0m')
        messageEncoded = jwt.encode({
        'id': 1,
        'username': 'cool'}, 'password', algorithm='HS256')
        make_test(lambda: jwt.decode(messageEncoded, 'password', algorithms=['HS256']))(JwtTest, 'Decode Message', False)
        make_test(lambda: jwt.decode(messageEncoded, 'wrongpassword', algorithms=['HS256']))(JwtTest, 'Incorrect password', True)
        make_test(lambda: jwt.decode(messageEncoded+'z', 'password', algorithms=['HS256']))(JwtTest, 'Incorrect encoded message', True)

    def checkDifferentSignatures():
        print('\033[01m## Creation ##\033[0m')
        messageEncoded = jwt.encode({
            'id': 1,
            'username': 'user'}, 'password', algorithm='HS256')
        secondMessageEncoded = jwt.encode({
            'id': 1,
            'username': 'user'}, 'anotherPassword', algorithm='HS256')
        make_test(lambda: messageEncoded != secondMessageEncoded)(JwtTest, 'Different Password + Different Signature', False)
        messageEncoded = jwt.encode({
            'id': 1,
            'username': 'firstUser'}, 'password', algorithm='HS256')
        secondMessageEncoded = jwt.encode({
            'id': 2,
            'username': 'secondUser'}, 'password', algorithm='HS256')
        make_test(lambda: messageEncoded != secondMessageEncoded)(JwtTest, 'Different Payload + Different Signature', False)

if __name__ == '__main__':
    JwtTest.encodeDocument()
    JwtTest.decodeDocument()
    JwtTest.checkDifferentSignatures()
    print('\n\n\033[04mSuccess\033[01m: ',
          JwtTest.nb_tests_succeed, '/',
          JwtTest.nb_tests, sep='')
#!/usr/bin/env python3
# coding: utf8


class LoginError(Exception):
    pass


class FormatError(Exception):
    pass


class AuthError(Exception):
    pass


class SuccessNoBody(Exception):
    pass


class NotFound(Exception):
    pass


def throw(ex):
    """
    Transforms a raise statement into an expression. Used in lambda functions
    because they can only have an expression
    :param ex: An exception
    :return: Nothing, will always raise
    :raises: The exception passed as parameter
    """
    raise ex
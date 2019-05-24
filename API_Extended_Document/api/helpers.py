#!/usr/bin/env python3
# coding: utf8

from util.Exception import *
from util.log import *
from util.VarConfig import *

from flask import jsonify, request
import sqlalchemy.exc
import sqlalchemy.orm
import jwt

from functools import wraps


class Response:
    """
    Represents a response that can be handled y Flask. It contains a 'content',
    which should be a string, a dict or a list. If it is a dict or a list,
    the content will be formatted into a JSON format thanks to the 'jsonify'
    method from flask.
    """
    def __init__(self, content):
        if isinstance(content, (dict, list)):
            self.content = jsonify(content)
        else:
            self.content = content

    def format(self):
        """
        Format the response for Flask. Should not be called from the
        superclass. Should be overridden by subclasses to return the content
        and an error code.
        """
        raise NotImplementedError("Cannot send an abstract Response. Please "
                                  "send a subclass instead.")


class ResponseOK(Response):
    """
    Represents a HTTP 200 OK response. See the `Response` superclass for more
    information.
    """
    def format(self):
        return self.content, 200


class ResponseCreated(Response):
    """
    Represents a HTTP 201 CREATED response. See the `Response` superclass for
    more information.
    """
    def format(self):
        return self.content, 201


class ResponseNoContent(Response):
    """
    Represents a HTTP 204 NO CONTENT response. As no content should be provided
    with this kind of response, the constructor does not take any argument.
    """
    def __init__(self):
        super().__init__('')

    def format(self):
        return '', 204


def format_response(old_function, authorization_function=None,
                    authorization=None, resource_id=None):
    """
    Decorator used to format the response of `old_function` into a Flask
    response tuple. `old_function` should either return a `Response` object
    or raise an exception.
    :param old_function: The old function.
    :param authorization_function:
    :param authorization:
    :param resource_id:
    :return: A new function which returns a Flask response.
    """
    @wraps(old_function)
    def new_function(*args, **kwargs):
        try:
            if authorization_function:
                authorization_function(authorization, resource_id)
            response = old_function(*args, **kwargs)
            if isinstance(response, Response):
                return response.format()
            else:
                print('You should not return objects other than `Response`')
                info_logger.warn('You should not return objects other than'
                                 '`Response`')
                return response
        except BadRequest as e:
            return f'Bad request\n{e}', 400
        except LoginError as e:
            return f'Unauthorized\n{e}', 401
        except AuthError as e:
            return f'Forbidden\n{e}', 403
        except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.DataError) as e:
            return f'Integrity error\n{e}', 422
        except (NotFound, sqlalchemy.orm.exc.NoResultFound) as e:
            return f'Not found\n{e}', 404
        except FormatError as e:
            return f'Unsupported file format\n{e}', 415
        except Exception as e:
            info_logger.error(e)
            return f"Unexpected error\n{e}", 500

    return new_function


def need_authentication(old_function):
    """
    Decorator used to specify that a route needs authentication. To put after
    the `app.route` decorator from Flask. Will search in the request headers
    for an 'Authorization' field and decode it as JWT. If the field cannot be
    found, or the timeout is expired, or the field is not a valid JWT, returns
    a LoginError.
    :param old_function: The old function
    :return: Either the old function, or a function that raises a LoginError
    """
    @wraps(old_function)
    def new_function(*args, **kwargs):
        try:
            # Can raise a KeyError if header is not found
            encoded_jwt = request.headers["Authorization"]
            decoded_jwt = jwt.decode(encoded_jwt, VarConfig.get()['password'],
                                     algorithms=['HS256'])
            if decoded_jwt is None:
                raise LoginError

            kwargs['auth_info'] = decoded_jwt
            return old_function(*args, **kwargs)
        except jwt.PyJWTError as e:
            raise LoginError(e)
        except KeyError:
            raise LoginError("Missing 'Authorization' header")
        except Exception as e:
            raise e

    return new_function

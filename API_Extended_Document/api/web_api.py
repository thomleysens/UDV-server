#!/usr/bin/env python3
# coding: utf8

import sqlalchemy.exc
import sqlalchemy.orm

from flask import Flask, send_from_directory, request
from flask.json import jsonify
from flask_cors import CORS

from controller.CommentController import CommentController
from controller.Controller import Controller
from controller.TourController import TourController
from controller.UserController import UserController
from controller.DocController import DocController
from controller.ArchiveController import ArchiveController
from util.upload import *
from util.encryption import *
from util.Exception import *
from util.JsonIsoEncoder import JsonIsoEncoder

from functools import wraps

app = Flask(__name__)
app.json_encoder = JsonIsoEncoder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


def format_response(old_function, authorization_function=None,
                    authorization=None, resource_id=None):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        try:
            if authorization_function:
                authorization_function(authorization, resource_id)
            response = old_function(*args, **kwargs)
            if response is None:
                return '', 204
            if isinstance(response, (dict, list)):
                return jsonify(response)
            return response
        except BadRequest as e:
            return f'Bad request\n{e}', 400
        except LoginError as e:
            return f'Unauthorized\n{e}', 401
        except AuthError as e:
            return f'Forbidden\n{e}', 403
        except sqlalchemy.exc.IntegrityError as e:
            return f'Integrity error\n{e}', 422
        except sqlalchemy.orm.exc.NoResultFound as e:
            return f'No result found\n{e}', 404
        except NotFound as e:
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


@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
      <body>
        <h1 style="text-align:center">
          Welcome on API-ExtendedDocument
        </h1>
        <div style="text-align:center">
          <p> This application was developed by MEPP team </p>
          <a href="https://github.com/MEPP-team/UDV-server/tree/master/API_Extended_Document"
             style="text-align:center"> Find us on Github! </a>
        </div>
      </body>
    </html>
    '''


@app.route('/login', methods=['POST'])
@format_response
def login():
    return UserController.login(
            {key: request.form.get(key) for key in
             request.form.keys()})


@app.route('/user', methods=['POST'])
@format_response
def create_user():
    return UserController.create_user(
            {key: request.form.get(key) for key in
             request.form.keys()})


@app.route('/user/me', methods=['GET'])
@format_response
@need_authentication
def get_connected_user(auth_info):
    return UserController.get_user_by_id(auth_info['user_id'])


@app.route('/user/<int:user_id>', methods=['GET'])
@format_response
def get_user(user_id):
    return UserController.get_user_by_id(user_id)


@app.route('/user/grant', methods=['POST'])
@format_response
@need_authentication
def add_privileged_user(auth_info):
    return UserController.create_privileged_user({
            key: request.form.get(key) for key in
            request.form.keys()}, auth_info)


@app.route('/document', methods=['POST'])
@format_response
@need_authentication
def create_document(auth_info):
    args = {key: request.form.get(key) for key in
            request.form.keys()}
    args.update(auth_info)
    if request.files.get('file'):
        filename = save_file(request.files['file'])
        if filename is not None:
            args['file'] = filename
            document = DocController.create_document(args)
            return document
        else:
            raise FormatError("Invalid file format")
    else:
        raise BadRequest("Missing 'file' parameter")


@app.route('/document', methods=['GET'])
@format_response
def get_documents():
    return DocController.get_documents(
            {key: request.args.get(key)
             for key in request.args.keys()})


@app.route('/document/<int:doc_id>', methods=['GET'])
@format_response
def get_document(doc_id):
    return DocController.get_document_by_id(doc_id)


@app.route('/document/<int:doc_id>', methods=['PUT'])
@format_response
@need_authentication
def update_document(doc_id, auth_info):
    attributes = {key: request.form.get(key) for key in request.form.keys()}
    return DocController.update_document(auth_info, doc_id, attributes)


@app.route('/document/<int:doc_id>', methods=['DELETE'])
@format_response
@need_authentication
def delete_document(doc_id, auth_info):
    return DocController.delete_documents(doc_id, auth_info)


@app.route('/document/<int:doc_id>/comment', methods=['POST'])
@format_response
@need_authentication
def create_comment(doc_id, auth_info):
    form = {key: request.form.get(key) for key in request.form.keys()}
    args = {}
    args.update(auth_info)
    args.update(form)
    comment = CommentController.create_comment(doc_id, args)
    return comment


@app.route('/document/<int:doc_id>/comment', methods=['GET'])
@format_response
def get_comment(doc_id):
    return CommentController.get_comments(doc_id)


@app.route('/comment/<int:comment_id>', methods=['PUT'])
@format_response
@need_authentication
def update_comment(comment_id, auth_info):
    form = {key: request.form.get(key) for key in request.form.keys()}
    args = {}
    args.update(auth_info)
    args.update(form)
    comment = CommentController.update_comment(comment_id, args)
    return comment


@app.route('/comment/<int:comment_id>', methods=['DELETE'])
@format_response
@need_authentication
def delete_comment(comment_id, auth_info):
    return CommentController.delete_comment(comment_id, auth_info)


@app.route('/document/<int:doc_id>/archive', methods=['GET'])
@format_response
def get_archive(doc_id):
    return ArchiveController.get_archive(doc_id)


@app.route('/document/validate', methods=['POST'])
@format_response
@need_authentication
def validate_document(auth_info):
    return DocController.validate_document(
            request.form['id'], auth_info)


@app.route('/document/in_validation', methods=['GET'])
@format_response
@need_authentication
def get_documents_to_validate(auth_info):
    return DocController.get_documents_to_validate(auth_info)


@app.route('/document/<int:doc_id>/file', methods=['GET'])
@format_response
def get_document_file(doc_id):
    location = DocController.get_document_file_location(doc_id)
    return send_from_directory(os.getcwd(), location)


@app.route('/document/<int:doc_id>/file', methods=['POST'])
@format_response
def upload_file(doc_id):
    if request.files.get('file'):
        file = request.files['file']
        return save_file(doc_id, file)
    else:
        raise BadRequest("Missing 'file' data")


@app.route('/document/<doc_id>/file', methods=['DELETE'])
@format_response
def delete_member_image(doc_id):
    return delete_image(doc_id)


@app.route('/guidedTour', methods=['POST'])
@format_response
def create_guided_tour():
    name = request.form.get('name')
    description = request.form.get('description')
    if name is None or description is None:
        raise BadRequest("Parameters are missing : 'name', 'description'")

    return TourController.create_tour(name, description)


@app.route('/guidedTour', methods=['GET'])
@format_response
def get_all_guided_tours():
    return TourController.get_tours()


@app.route('/guidedTour/<int:tour_id>', methods=['GET'])
@format_response
def get_guided_tour(tour_id):
    return TourController.get_tour_by_id(tour_id)


@app.route('/guidedTour/<int:tour_id>', methods=['PUT'])
@format_response
def update_guided_tour(tour_id):
    return TourController.update(tour_id, request.form)


@app.route('/guidedTour/<int:doc_id>', methods=['DELETE'])
@format_response
def delete_tour(doc_id):
    return TourController.delete_tour(doc_id)


@app.route('/guidedTour/<int:tour_id>/document', methods=['POST'])
@format_response
def add_document_to_guided_tour(tour_id):
    doc_id = request.form.get('doc_id')
    if doc_id is None or tour_id is None:
        raise BadRequest("Parameter is missing : 'doc_id'")

    return TourController.add_document(tour_id, doc_id)


@app.route('/guidedTour/<int:tour_id>/document/<int:doc_position>',
           methods=['POST'])
@format_response
def update_guided_tour_document(tour_id, doc_position):
    return TourController.update_document(tour_id, doc_position, request.form)


if __name__ == '__main__':
    Controller.create_tables()
    app.run(debug=True, host='0.0.0.0')

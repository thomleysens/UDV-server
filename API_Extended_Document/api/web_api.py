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


def send_response(old_function, authorization_function=None,
                  authorization=None, resource_id=None):
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


def get_file(member_id):
    image_location = find_image(member_id)
    if image_location:
        return send_from_directory(
            safe_join(os.getcwd(), app.config['UPLOAD_FOLDER']),
            image_location)
    raise NotFound


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
                return send_response(lambda: throw(LoginError))()

            kwargs['user'] = decoded_jwt
            return old_function(*args, **kwargs)
        except jwt.PyJWTError as e:
            return send_response(lambda: throw(LoginError(e)))()
        except KeyError:
            return send_response(lambda: throw(LoginError("Missing 'Authorization' header")))()
        except Exception as e:
            return send_response(lambda: throw(e))()

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
def login():
    return send_response(
        lambda: UserController.login(
            {key: request.form.get(key) for key in
             request.form.keys()}))()


@app.route('/user', methods=['POST'])
def create_user():
    return send_response(
        lambda: UserController.create_user(
            {key: request.form.get(key) for key in
             request.form.keys()}))()


@app.route('/user/me', methods=['GET'])
@need_authentication
def get_connected_user(user):
    return send_response(
        lambda: UserController.get_user_by_id(user['user_id']))()


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return send_response(
        lambda: UserController.get_user_by_id(user_id))()


@app.route('/user/grant', methods=['POST'])
@need_authentication
def add_privileged_user(user):
    return send_response(
        lambda: UserController.create_privileged_user({
            key: request.form.get(key) for key in
            request.form.keys()}, user))()


@app.route('/document', methods=['POST'])
@need_authentication
def create_document(user):
    def creation():
        args = {key: request.form.get(key) for key in
                request.form.keys()}
        args.update(user)
        document = DocController.create_document(args)
        filename = ''
        if request.files.get('file'):
            filename = save_file(document['id'],
                                 request.files['file'])
        if filename is not None:
            payload = user
            payload['file'] = filename
            payload['initial_creation'] = True
            document = DocController.update_document(document['id'],
                                                     payload)
        else:
            raise FormatError
        return document

    return send_response(lambda: creation())()


@app.route('/document', methods=['GET'])
def get_documents():
    return send_response(
        lambda: DocController.get_documents(
            {key: request.args.get(key)
             for key in request.args.keys()}))()


@app.route('/document/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    return send_response(
        lambda: DocController.get_document_by_id(doc_id))()


@app.route('/document/<int:doc_id>', methods=['PUT'])
@need_authentication
def update_document(doc_id, user):
    args = {key: request.form.get(key) for key in request.form.keys()}
    args['initial_creation'] = False
    args.update(user)
    return send_response(
        lambda: DocController.update_document(doc_id, args))()


@app.route('/document/<int:doc_id>', methods=['DELETE'])
@need_authentication
def delete_document(doc_id, user):
    return send_response(lambda: DocController.delete_documents(
        doc_id, user))()


@app.route('/document/<int:doc_id>/comment', methods=['POST'])
@need_authentication
def create_comment(doc_id, user):
    def creation():
        payload = user
        form = {key: request.form.get(key) for key in request.form.keys()}
        args = {}
        args.update(payload)
        args.update(form)
        comment = CommentController.create_comment(doc_id, args)
        return comment

    return send_response(creation)()


@app.route('/document/<int:doc_id>/comment', methods=['GET']) 
def get_comment(doc_id):
    return send_response(
        lambda: CommentController.get_comments(doc_id))()


@app.route('/comment/<int:comment_id>', methods=['PUT'])
@need_authentication
def update_comment(comment_id, user):
    def creation():
        payload = user
        form = {key: request.form.get(key) for key in request.form.keys()}
        args = {}
        args.update(payload)
        args.update(form)
        comment = CommentController.update_comment(comment_id, args)
        return comment

    return send_response(creation)()


@app.route('/comment/<int:comment_id>', methods=['DELETE'])
@need_authentication
def delete_comment(comment_id, user):
    return send_response(lambda: CommentController.delete_comment(comment_id, user))()


@app.route('/document/<int:doc_id>/archive', methods=['GET'])
def get_archive(doc_id):
    return send_response(
        lambda: ArchiveController.get_archive(doc_id))()


@app.route('/document/validate', methods=['POST'])
@need_authentication
def validate_document(user):
    return send_response(
        lambda: DocController.validate_document(
            request.form['id'], user))()


@app.route('/document/in_validation', methods=['GET'])
@need_authentication
def get_documents_to_validate(user):
    return send_response(
        lambda: DocController.get_documents_to_validate(
            user))()


@app.route('/document/<int:doc_id>/file', methods=['GET'])
def get_document_file(doc_id):
    return send_response(
        lambda: get_file(doc_id)
    )()


@app.route('/document/<int:doc_id>/file', methods=['POST'])
def upload_file(doc_id):
    if request.files.get('file'):
        file = request.files['file']
        return send_response(
            lambda: save_file(doc_id, file)
        )()


@app.route('/document/<doc_id>/file', methods=['DELETE'])
def delete_member_image(doc_id):
    return send_response(
        lambda: delete_image(doc_id)
    )()


@app.route('/guidedTour', methods=['POST'])
def create_guided_tour():
    name = request.form.get('name')
    description = request.form.get('description')
    if name is None or description is None:
        return 'parameter is missing', 400

    return send_response(
        lambda: TourController.create_tour(name, description))()


@app.route('/guidedTour', methods=['GET'])
def get_all_guided_tours():
    return send_response(
        lambda: TourController.get_tours())()


@app.route('/guidedTour/<int:tour_id>', methods=['GET'])
def get_guided_tour(tour_id):
    return send_response(
        lambda: TourController.get_tour_by_id(tour_id))()


@app.route('/guidedTour/<int:tour_id>', methods=['PUT'])
def update_guided_tour(tour_id):
    return send_response(
        lambda: TourController.update(
            tour_id, request.form))()


@app.route('/guidedTour/<int:doc_id>', methods=['DELETE'])
def delete_tour(doc_id):
    return send_response(
        lambda: TourController.delete_tour(doc_id))()


@app.route('/guidedTour/<int:tour_id>/document', methods=['POST'])
def add_document_to_guided_tour(tour_id):
    doc_id = request.form.get('doc_id')
    if doc_id is None or tour_id is None:
        return 'parameter is missing', 400

    return send_response(
        lambda: TourController.add_document(tour_id, doc_id))()


@app.route('/guidedTour/<int:tour_id>/document/<int:doc_position>',
           methods=['POST'])
def update_guided_tour_document(tour_id, doc_position):
    return send_response(
        lambda: TourController.update_document(
            tour_id, doc_position, request.form))()


if __name__ == '__main__':
    Controller.create_tables()
    app.run(debug=True, host='0.0.0.0')

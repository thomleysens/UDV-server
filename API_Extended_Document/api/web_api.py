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

app = Flask(__name__)
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

        except LoginError:
            return 'unauthorized', 401
        except AuthError:
            return 'access denied', 403
        except sqlalchemy.exc.IntegrityError:
            return 'integrity error', 422
        except sqlalchemy.orm.exc.NoResultFound:
            return 'no result found', 204
        except (AuthError, jwt.exceptions.InvalidSignatureError):
            return 'Authentication failed', 403
        except NotFound:
            return 'no result found', 404
        except Exception as e:
            print(e)
            info_logger.error(e)
            return "unexpected error", 500

    return new_function


def get_file(member_id):
    image_location = find_image(member_id)
    if image_location:
        return send_from_directory(
            safe_join(os.getcwd(), app.config['UPLOAD_FOLDER']),
            image_location)
    raise NotFound


def is_connected(*args):
    encoded_jwt = args[0]["Authorization"]
    if encoded_jwt:
        payload = jwt.decode(encoded_jwt, VarConfig.get()['password'],
                             algorithms=['HS256'])
        if payload:
            return payload
    raise LoginError


def get_my_id(authorization):
    return is_connected(authorization)['user_id']


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
def get_connected_user():
    return send_response(
        lambda: UserController.get_user_by_id(
            is_connected(request.headers)['user_id']))()


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return send_response(
        lambda: UserController.get_user_by_id(user_id))()


@app.route('/user/grant', methods=['POST'])
def add_privileged_user():
    return send_response(
        lambda: UserController.create_privileged_user({
            key: request.form.get(key) for key in
            request.form.keys()}, is_connected(request.headers)))()


@app.route('/document', methods=['POST'])
def create_document():
    def creation():
        args = {key: request.form.get(key) for key in
                request.form.keys()}
        args.update(is_connected(request.headers))
        document = DocController.create_document(args)
        filename = ''
        if request.files.get('link'):
            filename = save_file(document['id'],
                                 request.files['link'])
        if filename:
            payload = is_connected(request.headers)
            payload['link'] = filename
            payload['initial_creation'] = True
            document = DocController.update_document(document['id'],
                                                     payload)
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
def update_document(doc_id):
    args = {key: request.form.get(key) for key in request.form.keys()}
    payload = is_connected(request.headers)
    args['initial_creation'] = False
    args.update(payload)
    return send_response(
        lambda: DocController.update_document(doc_id, args))()


@app.route('/document/<int:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    return send_response(lambda: DocController.delete_documents(
        doc_id, is_connected(request.headers)))()


@app.route('/document/<int:doc_id>/comment', methods=['POST'])
def create_comment(doc_id):
    def creation():
        payload = is_connected(request.headers)
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
def update_comment(comment_id):
    def creation():
        payload = is_connected(request.headers)
        form = {key: request.form.get(key) for key in request.form.keys()}
        args = {}
        args.update(payload)
        args.update(form)
        comment = CommentController.update_comment(comment_id, args)
        return comment

    return send_response(creation)()


@app.route('/comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    return send_response(lambda: CommentController.delete_comment(comment_id, is_connected(request.headers)))()


@app.route('/document/<int:doc_id>/archive', methods=['GET'])
def get_archive(doc_id):
    return send_response(
        lambda: ArchiveController.get_archive(doc_id))()


@app.route('/document/validate', methods=['POST'])
def validate_document():
    return send_response(
        lambda: DocController.validate_document(
            request.form['id'], is_connected(request.headers)))()


@app.route('/document/in_validation', methods=['GET'])
def get_documents_to_validate():
    return send_response(
        lambda: DocController.get_documents_to_validate(
            is_connected(request.headers)))()


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
            lambda: save(file, doc_id)
        )()


@app.route('/document/<doc_id>/file', methods=['DELETE'])
def delete_member_image(doc_id):
    return send_response(
        lambda: delete_image(doc_id)
    )()


@app.route('/guidedTour')
def create_guided_tour():
    name = request.args.get('name')
    description = request.args.get('description')
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


@app.route('/guidedTour/<int:tour_id>/document/<int:doc_position>', methods=['POST'])
def update_guided_tour_document(tour_id, doc_position):
    return send_response(
        lambda: TourController.update_document(
            tour_id, doc_position, request.form))()


if __name__ == '__main__':
    Controller.create_tables()
    app.run(debug=True, host='0.0.0.0')

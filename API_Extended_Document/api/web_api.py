#!/usr/bin/env python3
# coding: utf8

import sqlalchemy.exc
import sqlalchemy.orm
import jwt

from flask import Flask, send_from_directory, request, safe_join
from flask.json import jsonify
from flask_cors import CORS

from controller.Controller import Controller
from controller.TourController import TourController
from controller.UserController import UserController
from controller.DocController import DocController
from util.log import info_logger
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
    if jwt:
        payload = jwt.decode(encoded_jwt, VarConfig.get()['password'],
                             algorithms=['HS256'])
        if payload:
            return payload
    raise LoginError


def get_user_id(*args):
    print(is_connected())


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


@app.route('/addDocument', methods=['POST'])
def create_document():
    def creation():
        payload = jwt.decode(request.headers.get('Authorization'),
                             VarConfig.get()['password'],
                             algorithms=['HS256'])
        if payload:
            args = {key: request.form.get(key) for key in
                    request.form.keys()}
            args['user_position'] = payload['position']['label']
            args['user_id'] = payload['user_id']
            document = DocController.create_document(args)
            if request.files.get('link'):
                filename = save_file(document["id"],
                                     request.files['link'])
                if filename:
                    DocController.update_document(document["id"],
                                                  {"link": filename})
            return document
        else:
            raise LoginError

    return send_response(creation)()


@app.route('/addGuidedTour')
def create_guided_tour():
    name = request.args.get('name')
    description = request.args.get('description')
    if name is None or description is None:
        return 'parameter is missing', 400

    return send_response(
        lambda: TourController.create_tour(name, description))()


@app.route('/addUser', methods=['POST'])
def create_user():
    return send_response(
        lambda: UserController.create_user(
            {key: request.form.get(key) for key in
             request.form.keys()}))()


@app.route('/addPrivilegedUser', methods=['POST'])
def add_privileged_user():
    payload = jwt.decode(request.headers.get('Authorization'),
                         VarConfig.get()['password'],
                         algorithms=['HS256'])
    if payload:
        args = {key: request.form.get(key) for key in
                request.form.keys()}
        args['user_position'] = payload['position']['label']
        args['user_id'] = payload['user_id']
        return send_response(
            lambda: UserController.create_privileged_user(args))()
    else:
        raise AuthError


@app.route('/login', methods=['POST'])
def login():
    return send_response(
        lambda: UserController.login(
            {key: request.form.get(key) for key in
             request.form.keys()}))()


@app.route('/getDocument/<int:doc_id>', methods=['GET', 'POST'])
def get_document(doc_id):
    return send_response(
        lambda: DocController.get_document_by_id(doc_id))()


@app.route('/getUser/<int:user_id>', methods=['GET', 'POST'])
def get_user(user_id):
    return send_response(
        lambda: UserController.get_user_by_id(user_id))()


@app.route('/getGuidedTour/<int:tour_id>')
def get_guided_tour(tour_id):
    return send_response(
        lambda: TourController.get_tour_by_id(tour_id))()


@app.route('/getDocuments', methods=['GET', 'POST'])
def get_documents():
    return send_response(
        lambda: DocController.get_documents(
            {key: request.args.get(key)
             for key in request.args.keys()}))()


@app.route('/getDocuments_to_validate', methods=['GET', 'POST'])
def get_documents_to_validate():
    payload = jwt.decode(request.headers.get('Authorization'),
                         VarConfig.get()['password'],
                         algorithms=['HS256'])
    if payload:
        args = {key: request.form.get(key) for key in
                request.form.keys()}
        args['user_position'] = payload['position']['label']
        args['user_id'] = payload['user_id']
        return send_response(
            lambda: DocController.get_documents_to_validate(args))()
    else:
        raise AuthError


@app.route('/getGuidedTours', methods=['GET', 'POST'])
def get_all_guided_tours():
    return send_response(
        lambda: TourController.get_tours())()


@app.route('/editDocument/<int:doc_id>', methods=['POST'])
def update_document(doc_id):
    payload = jwt.decode(request.headers.get('Authorization'),
                         VarConfig.get()['password'],
                         algorithms=['HS256'])
    if payload:
        args = {key: request.form.get(key) for key in
                request.form.keys()}
        args['user_position'] = payload['position']['label']
        args['user_id'] = payload['user_id']
        return send_response(
            lambda: DocController.update_document(doc_id, args))()
    else:
        raise AuthError


@app.route('/validateDocument/<int:doc_id>', methods=['GET'])
def validate_document(doc_id):
    payload = jwt.decode(request.headers.get('Authorization'),
                         VarConfig.get()['password'],
                         algorithms=['HS256'])
    if payload:
        return send_response(
            lambda: DocController.validate_document(doc_id, {
                'user_position': payload['position']['label'], 'user_id': int(payload['user_id'])}))()
    else:
        raise AuthError


@app.route('/addDocumentToGuidedTour')
def add_document_to_guided_tour():
    tour_id = request.args.get("tour_id")
    doc_id = request.args.get('doc_id')
    if doc_id is None or tour_id is None:
        return 'parameter is missing', 400

    return send_response(
        lambda: TourController.add_document(tour_id, doc_id))()


@app.route('/editGuidedTour/<int:tour_id>', methods=['POST'])
def update_guided_tour(tour_id):
    return send_response(
        lambda: TourController.update(
            tour_id, request.form))()


@app.route('/editGuidedTourDocument/<int:tour_id>', methods=['POST'])
def update_guided_tour_document(tour_id):
    doc_position = int(request.form.get('doc_position'))
    return send_response(
        lambda: TourController.update_document(
            tour_id, doc_position, request.form))()


@app.route('/deleteGuidedTour/<int:doc_id>')
def delete_tour(doc_id):
    return send_response(
        lambda: TourController.delete_tour(doc_id))()


@app.route('/deleteDocument/<int:doc_id>')
def delete_document(doc_id):
    payload = jwt.decode(request.headers.get('Authorization'),
                         VarConfig.get()['password'],
                         algorithms=['HS256'])
    if payload:
        return send_response(
            lambda: DocController.delete_documents(doc_id, {
                'user_position': payload['position']['label'], 'user_id': int(payload['user_id'])}))()
    else:
        raise AuthError


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


@app.route('/getFile/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(
        safe_join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


if __name__ == '__main__':
    Controller.create_tables()
    app.run(debug=True, host='0.0.0.0')

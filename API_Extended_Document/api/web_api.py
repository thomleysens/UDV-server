#!/usr/bin/env python3
# coding: utf8

from flask import Flask, send_from_directory
from flask_cors import CORS

from controller.CommentController import CommentController
from controller.Controller import Controller
from controller.TourController import TourController
from controller.UserController import UserController
from controller.DocController import DocController
from controller.ArchiveController import ArchiveController
from util.upload import *
from util.JsonIsoEncoder import JsonIsoEncoder

# Imports the Response objects and the need_authentication / format_response
# decorators
from helpers import *

app = Flask(__name__)
app.json_encoder = JsonIsoEncoder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


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
    token = UserController.login(
            {key: request.form.get(key) for key in
             request.form.keys()})
    return ResponseOK(token)


@app.route('/user', methods=['POST'])
@format_response
def create_user():
    created_user = UserController.create_user(
            {key: request.form.get(key) for key in
             request.form.keys()})
    return ResponseCreated(created_user)


@app.route('/user/me', methods=['GET'])
@format_response
@need_authentication
def get_connected_user(auth_info):
    user = UserController.get_user_by_id(auth_info['user_id'])
    return ResponseOK(user)


@app.route('/user/<int:user_id>', methods=['GET'])
@format_response
def get_user(user_id):
    user = UserController.get_user_by_id(user_id)
    return ResponseOK(user)


@app.route('/user/grant', methods=['POST'])
@format_response
@need_authentication
def add_privileged_user(auth_info):
    user = UserController.create_privileged_user({
            key: request.form.get(key) for key in
            request.form.keys()}, auth_info)
    return ResponseOK(user)


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
            return ResponseCreated(document)
        else:
            raise FormatError("Invalid file format")
    else:
        raise BadRequest("Missing 'file' parameter")


@app.route('/document', methods=['GET'])
@format_response
def get_documents():
    documents = DocController.get_documents(
            {key: request.args.get(key)
             for key in request.args.keys()})
    return ResponseOK(documents)


@app.route('/document/<int:doc_id>', methods=['GET'])
@format_response
def get_document(doc_id):
    document = DocController.get_document_by_id(doc_id)
    return ResponseOK(document)


@app.route('/document/<int:doc_id>', methods=['PUT'])
@format_response
@need_authentication
def update_document(doc_id, auth_info):
    attributes = {key: request.form.get(key) for key in request.form.keys()}
    updated_document = DocController.update_document(auth_info, doc_id,
                                                     attributes)
    return ResponseOK(updated_document)


@app.route('/document/<int:doc_id>', methods=['DELETE'])
@format_response
@need_authentication
def delete_document(doc_id, auth_info):
    deleted_document = DocController.delete_documents(doc_id, auth_info)
    return ResponseOK(deleted_document)


@app.route('/document/<int:doc_id>/comment', methods=['POST'])
@format_response
@need_authentication
def create_comment(doc_id, auth_info):
    form = {key: request.form.get(key) for key in request.form.keys()}
    args = {}
    args.update(auth_info)
    args.update(form)
    comment = CommentController.create_comment(doc_id, args)
    return ResponseCreated(comment)


@app.route('/document/<int:doc_id>/comment', methods=['GET'])
@format_response
def get_comment(doc_id):
    comments = CommentController.get_comments(doc_id)
    return ResponseOK(comments)


@app.route('/comment/<int:comment_id>', methods=['GET'])
@format_response
def get_comment_by_id(comment_id):
    comment = CommentController.get_comment(comment_id)
    return ResponseOK(comment)


@app.route('/comment/<int:comment_id>', methods=['PUT'])
@format_response
@need_authentication
def update_comment(comment_id, auth_info):
    form = {key: request.form.get(key) for key in request.form.keys()}
    args = {}
    args.update(auth_info)
    args.update(form)
    updated_comment = CommentController.update_comment(comment_id, args)
    return ResponseOK(updated_comment)


@app.route('/comment/<int:comment_id>', methods=['DELETE'])
@format_response
@need_authentication
def delete_comment(comment_id, auth_info):
    deleted_comment = CommentController.delete_comment(comment_id, auth_info)
    return ResponseOK(deleted_comment)


@app.route('/document/<int:doc_id>/archive', methods=['GET'])
@format_response
def get_archive(doc_id):
    archive = ArchiveController.get_archive(doc_id)
    return ResponseOK(archive)


@app.route('/document/validate', methods=['POST'])
@format_response
@need_authentication
def validate_document(auth_info):
    validated_document = DocController.validate_document(
                         request.form['id'], auth_info)
    return ResponseOK(validated_document)


@app.route('/document/in_validation', methods=['GET'])
@format_response
@need_authentication
def get_documents_to_validate(auth_info):
    documents = DocController.get_documents_to_validate(auth_info)
    return ResponseOK(documents)


# This method does not follow the standard scheme because of the
# `send_from_directory` flask method (hence neither `format_response` nor
# a `Response` object are present).
@app.route('/document/<int:doc_id>/file', methods=['GET'])
def get_document_file(doc_id):
    location = DocController.get_document_file_location(doc_id)
    return send_from_directory(os.getcwd(), location)


@app.route('/document/<int:doc_id>/file', methods=['POST'])
@format_response
@need_authentication
def upload_file(doc_id, auth_info):
    if request.files.get('file'):
        file = request.files['file']
        filename = save_file(file)
        updated_document = DocController.update_document(auth_info, doc_id, {
            'file': filename
        })
        return ResponseOK(updated_document)
    else:
        raise BadRequest("Missing 'file' data")


@app.route('/document/<doc_id>/file', methods=['DELETE'])
@format_response
@need_authentication
def delete_member_image(doc_id, auth_info):
    filename = DocController.get_document_file_location(doc_id)
    document = DocController.delete_document_file(auth_info, doc_id)
    delete_file(filename)
    return ResponseOK(document)


@app.route('/guidedTour', methods=['POST'])
@format_response
def create_guided_tour():
    name = request.form.get('name')
    description = request.form.get('description')
    if name is None or description is None:
        raise BadRequest("Parameters are missing : 'name', 'description'")

    guided_tour = TourController.create_tour(name, description)
    return ResponseCreated(guided_tour)


@app.route('/guidedTour', methods=['GET'])
@format_response
def get_all_guided_tours():
    guided_tours = TourController.get_tours()
    return ResponseOK(guided_tours)


@app.route('/guidedTour/<int:tour_id>', methods=['GET'])
@format_response
def get_guided_tour(tour_id):
    guided_tour = TourController.get_tour_by_id(tour_id)
    return ResponseOK(guided_tour)


@app.route('/guidedTour/<int:tour_id>', methods=['PUT'])
@format_response
def update_guided_tour(tour_id):
    updated_tour = TourController.update(tour_id, request.form)
    return ResponseOK(updated_tour)


@app.route('/guidedTour/<int:doc_id>', methods=['DELETE'])
@format_response
def delete_tour(doc_id):
    deleted_tour = TourController.delete_tour(doc_id)
    return ResponseOK(deleted_tour)


@app.route('/guidedTour/<int:tour_id>/document', methods=['POST'])
@format_response
def add_document_to_guided_tour(tour_id):
    doc_id = request.form.get('doc_id')
    if doc_id is None or tour_id is None:
        raise BadRequest("Parameter is missing : 'doc_id'")

    guided_tour = TourController.add_document(tour_id, doc_id)
    return ResponseCreated(guided_tour)


@app.route('/guidedTour/<int:tour_id>/document/<int:doc_position>',
           methods=['POST'])
@format_response
def update_guided_tour_document(tour_id, doc_position):
    updated_tour = TourController.update_document(tour_id, doc_position, request.form)
    return ResponseOK(updated_tour)


@app.route('/guidedTour/<int:tour_id>/document/<int:doc_position>',
           methods=['DELETE'])
@format_response
def delete_guided_tour_document(tour_id, doc_position):
    updated_tour = TourController.remove_document(tour_id, doc_position)
    return ResponseOK(updated_tour)


if __name__ == '__main__':
    Controller.create_tables()
    app.run(debug=True, host='0.0.0.0')

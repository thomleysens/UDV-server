#!/usr/bin/env python3
# coding: utf8

from flask import Flask, request
from flask.json import jsonify

from util.log import *
from controller.Controller import Controller

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


@app.route('/addDocument', methods=['GET'])
def create_document():
    try:
        Controller.create_document(
            {key: request.args.get(key) for key in
             request.args.keys()})
        return 'success'
    except Exception as e:
        info_logger.error(e)
        return 'error', 404


@app.route('/getDocument/<int:doc_id>', methods=['GET', 'POST'])
def get_document(doc_id):
    try:
        return jsonify(Controller.serialize(
            Controller.get_document_by_id(doc_id)))
    except Exception as e:
        info_logger.error(e)
        return 'error', 404


@app.route('/getDocuments', methods=['GET'])
def get_documents():
    try:
        if request.args.get("keyword"):
            return jsonify(Controller.serialize((
                Controller.get_documents_by_keyword(
                    request.args.get('keyword')))))
        else:
            return jsonify(
                Controller.serialize(Controller.get_documents(
                    {key: request.args.get(key) for key in
                     request.args.keys()})))
    except Exception as e:
        info_logger.error(e)
        return 'error', 404


@app.route('/editDocument/<int:doc_id>', methods=['POST'])
def update_document(doc_id):
    Controller.update_document(doc_id, request.form)
    return 'success'


@app.route('/deleteDocument/<int:doc_id>')
def delete_document(doc_id):
    Controller.delete_documents(doc_id)
    return 'success'


if __name__ == '__main__':
    app.run(debug=True)

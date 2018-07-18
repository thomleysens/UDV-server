#!/usr/bin/env python3
# coding: utf8

from flask import Flask, send_from_directory, redirect, request, safe_join
from flask.json import jsonify
from flask_cors import CORS

from util.log import *
from util.upload import *
from controller.Controller import Controller

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
      <body>        
        <h1 style="text-align:center"> Welcome on API-ExtendedDocument </h1>
        <div style="text-align:center">
          <p> This application was developped by MEEP team </p>
          <a href="https://github.com/MEPP-team/UDV-server/tree/master/API_Extended_Document" 
             style="text-align:center"> Find us on Github! </a>
        </div>
      </body>
    </html>
    '''


@app.route('/addDocument', methods=['POST'])
def create_document():
    try:
        document = Controller.create_document(
            {key: request.form.get(key) for key in request.form.keys()})

        if request.files.get('link'):
            filename = save_file(document["id"], request.files['link'])
            if filename:
                Controller.update_document(document["id"],
                                           {"link": filename})
                return "success", 200
        return 'error', 404
    except Exception as e:
        info_logger.error(e)
        return 'error', 404


@app.route('/getDocument/<int:doc_id>', methods=['GET', 'POST'])
def get_document(doc_id):
    try:
        return jsonify(Controller.get_document_by_id(doc_id))
    except Exception as e:
        info_logger.error(e)
        return 'error', 404


@app.route('/getDocuments', methods=['GET', 'POST'])
def get_documents():
    try:
        return jsonify(Controller.get_documents(
            {key: request.args.get(key)
             for key in request.args.keys()}))
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


@app.route('/uploadFile/<int:doc_id>', methods=['GET', 'POST'])
def upload_file(doc_id):
    if request.method == 'POST':
        if request.files.get('file'):
            file = request.files['file']
            save_file(doc_id, file)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

import os
@app.route('/documents_directory/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(safe_join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


if __name__ == '__main__':
    app.run(debug=True)

#!/usr/bin/env python3
# coding: utf8

from flask import Flask, send_from_directory, redirect, request
from flask.json import jsonify
from flask_cors import CORS

from util.log import *
from util.upload import *
from controller.DocController import DocController

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


@app.route('/')
def index():
    return redirect(("https://github.com/laurenttainturier/"
                     "UDV-server/tree/master/API_Extended_Document"))
    # @TODO: To be replace with :
    # return redirect(("https://github.com/MEEP-Team/"
    #                  "UDV-server/tree/master/API_Extended_Document"))


@app.route('/addDocument', methods=['POST'])
def create_document():
    try:
        document = DocController.create_document(
            {key: request.form.get(key) for key in request.form.keys()})

        if request.files.get('link'):
            filename = save_file(document["id"], request.files['link'])
            if filename:
                DocController.update_document(document["id"],
                                              {"link": filename})
                return "success", 200
        return 'error', 404
    except Exception as e:
        info_logger.error(e)
        return 'error', 404


@app.route('/getDocument/<int:doc_id>', methods=['GET', 'POST'])
def get_document(doc_id):
    try:
        return jsonify(DocController.get_document_by_id(doc_id))
    except Exception as e:
        info_logger.error(e)
        return 'error', 404


@app.route('/getDocuments', methods=['GET', 'POST'])
def get_documents():
    try:
        return jsonify(DocController.get_documents(
            {key: request.args.get(key)
             for key in request.args.keys()}))
    except Exception as e:
        info_logger.error(e)
        return 'error', 404


@app.route('/editDocument/<int:doc_id>', methods=['POST'])
def update_document(doc_id):
    DocController.update_document(doc_id, request.form)
    return 'success'


@app.route('/deleteDocument/<int:doc_id>')
def delete_document(doc_id):
    DocController.delete_documents(doc_id)
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


@app.route('/documents_repository/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)

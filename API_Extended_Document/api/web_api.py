#!/usr/bin/env python3
# coding: utf8

from flask import Flask, request, send_from_directory
from flask.json import jsonify

from util.log import *
from util.upload import *
from controller.Controller import Controller

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return 'index'


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
        response = jsonify(Controller.get_document_by_id(doc_id))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        info_logger.error(e)
        return 'error', 404


@app.route('/getDocuments', methods=['GET', 'POST'])
def get_documents():
    try:
        response = jsonify(Controller.get_documents(
            {key: request.args.get(key)
             for key in request.args.keys()}))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
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


@app.route('/addDocument/<int:doc_id>', methods=['POST', 'GET'])
def upload_file1(doc_id):
    # @TODO: to be repaired
    if request.method == 'POST':
        # check if the post request has the file part

        if 'file' not in request.files:
            print('No file part')
            return "error"

        file = request.files['link']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "error"
        elif file:
            extension = get_extension(file.filename)
            if allowed_file(extension):
                filename = str(doc_id) + '.' + extension
                file.save(
                    os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return filename
        else:
            return "error"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=link>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/documents_repository/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)

#!/usr/bin/env python3
# coding: utf8

import sqlalchemy.exc
import sqlalchemy.orm
import psycopg2

from flask import Flask, send_from_directory, request, safe_join
from flask.json import jsonify
from flask_cors import CORS

from controller.TourController import TourController
from util.log import *
from util.upload import *
from controller.DocController import DocController

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


def send_response(old_function):
    def new_function(*args, **kwargs):
        try:
            return jsonify(old_function(*args, **kwargs))
        except psycopg2.IntegrityError:
            return 'integrity error', 422
        except sqlalchemy.orm.exc.NoResultFound:
            return 'no result found', 204
        except Exception as e:
            info_logger.error(e)
            return "unexpected error", 500

    return new_function


@send_response
def make_operation(operation_to_make):
    return operation_to_make()


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
          <p> This application was developed by MEEP team </p>  
          <a href="https://github.com/MEPP-team/UDV-server/tree/master/API_Extended_Document"   
             style="text-align:center"> Find us on Github! </a>  
        </div>  
      </body>  
    </html>  
    '''


@app.route('/addDocument', methods=['POST'])
def create_document():
    def creation():
        document = DocController.create_document(
            {key: request.form.get(key) for key in request.form.keys()})

        if request.files.get('link'):
            filename = save_file(document["id"], request.files['link'])
            if filename:
                DocController.update_document(document["id"],
                                              {"link": filename})
        return document

    return send_response(creation)()


@app.route('/addGuidedTour')
def create_guided_tour():
    name = request.args.get('name')
    description = request.args.get('description')
    if name is None or description is None:
        return 'parameter is missing', 400

    return send_response(
        lambda: TourController.create_tour(name, description))()


@app.route('/getDocument/<int:doc_id>', methods=['GET', 'POST'])
def get_document(doc_id):
    return send_response(
        lambda: DocController.get_document_by_id(doc_id))()


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


@app.route('/getGuidedTours', methods=['GET', 'POST'])
def get_all_guided_tours():
    return send_response(
        lambda: TourController.get_tours())()


@app.route('/editDocument/<int:doc_id>', methods=['POST'])
def update_document(doc_id):
    return send_response(
        lambda: DocController.update_document(doc_id, request.form))()


@app.route('/addDocumentToGuidedTour')
def add_document_to_guided_tour():
    tour_id = request.args.get("tour_id")
    doc_id = request.args.get('doc_id')
    if doc_id is None or tour_id is None:
        return 'parameter is missing', 400

    return send_response(
        lambda: TourController.add_document(tour_id, doc_id))()


@app.route('/editGuidedTourDocument/<int:tour_id>', methods=['GET', 'POST'])
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
    return send_response(
        lambda: DocController.delete_documents(doc_id))()


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
    return send_from_directory(
        safe_join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


if __name__ == '__main__':
    app.run(debug=True)

from logger import LOGGER
import os
import werkzeug
from flask import request, send_from_directory, make_response, jsonify
from flask_restful import reqparse, abort, Resource
from werkzeug.utils import secure_filename

import aws_client

TODOS = {
    'GET_All': {'GET': '/files - retrieves a list of files from AWS S3 bucket'},
    'GET_Specific': {'GET': '/files/:file - retrieves a specific file'},
    'POST': {'POST': '/files - uploads file into S3 bucket'},
    'DELETE': {'DELETE': '/files/:file - deletes a specific file from S3 bucket'},
}

def abort_if_todo_doesnt_exist(file_id):
    if file_id not in TODOS:
        abort(404, message='Resource API URL does not exist'.format(file_id))

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files',
                     required=True, help='required argument not set in request body')

class API(Resource):
    def get(self, file_id=''):
        try:
            if file_id == '':
                files = aws_client.listing_bucket(filename=file_id)
                LOGGER.error(f"Flask app: {str(request.method)} : {str(TODOS.get('GET_All'))} : {files}")
                return jsonify([{str(TODOS.get('GET_All')): str(files)}, {"AWS S3 Bucket": aws_client.s3_bucket}, 200])
            found = aws_client.listing_bucket(filename=file_id)
            LOGGER.info(f"Flask app: {str(request.method)} : {str(TODOS.get('GET_Specific'))} : File present: {found}")
            if found:
                found = aws_client.download_from_bucket(file_id)
                LOGGER.info(f"Flask app: {str(request.method)} : {str(TODOS.get('GET_Specific'))} : File download: {found}")
                try:
                    return make_response(send_from_directory(f'{os.getcwd()}/downloads', filename=file_id, as_attachment=True), 202)
                except FileNotFoundError:
                    LOGGER.exception("FileNotFoundError in Flask REST API call")
                    abort_if_todo_doesnt_exist(file_id)
        except Exception:
                LOGGER.exception("Exception in Flask REST API call")
                return jsonify([{str(TODOS.get('GET_Specific')): "File not available"}, {"AWS S3 Bucket": aws_client.s3_bucket}, 400])

    def delete(self, file_id=''):
        if file_id == '':
            abort_if_todo_doesnt_exist(file_id)
        try:
            delete_file = f'{os.getcwd()}/downloads/{file_id}'
            if os.path.exists(delete_file):
                os.remove(delete_file)
                LOGGER.info(f"Flask app: {str(request.method)} : File deleted in /downloads folder")
            delete_file = f'{os.getcwd()}/uploads/{file_id}'
            if os.path.exists(delete_file):
                os.remove(delete_file)
                LOGGER.info(f"Flask app: {str(request.method)} : File deleted in /uploads folder")
            deleted = aws_client.delete_into_bucket(file_id)
            LOGGER.info(f"Flask app: {str(request.method)} : {str(TODOS.get('DELETE'))} : File delete: {deleted}")
            if deleted:
                return jsonify([{str(TODOS.get('DELETE')): "File-delete successful"}, {"AWS S3 Bucket": aws_client.s3_bucket}, 200])
        except Exception:
            LOGGER.exception("Exception in Flask REST API call")
        return jsonify([{str(TODOS.get('DELETE')): "File-delete failed"}, {"AWS S3 Bucket": aws_client.s3_bucket}, 400])

    def post(self, file_id=''):
        if file_id != '':
            abort_if_todo_doesnt_exist(file_id)
        try:
            args = parser.parse_args()
            file = args['file']
            filename = secure_filename(file.filename)
            file.save(f'{os.getcwd()}/uploads/{filename}')
            saved = aws_client.upload_to_bucket(filename)
            LOGGER.info(f"Flask app: {str(request.method)} : {str(TODOS.get('POST'))} : File saved: {saved}")
            if saved:
                return jsonify([{str(TODOS.get('POST')): "File-upload successful"}, {"AWS S3 Bucket": aws_client.s3_bucket}, 201])
        except Exception:
            LOGGER.exception("Exception in Flask REST API call")
        return jsonify([{str(TODOS.get('POST')): "File-upload failed"}, {"AWS S3 Bucket": aws_client.s3_bucket}, 400])




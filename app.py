import os
import shutil

import werkzeug
from flask import Flask
from flask_restful import Api


from api import API
from logger import LOGGER
import aws_client


app = Flask(__name__.split('.')[0])
LOGGER.info("CALL Flask Module")

api = Api(app)
api.add_resource(API, '/files', '/files/', '/files/<path:file_id>')
app.logger.addHandler(LOGGER)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400

def create_new_folder(newpath):
    local_dir = newpath
    if os.path.exists(newpath):
        shutil.rmtree(newpath)
        LOGGER.info(f"Flask app: Local Folder: {newpath} - Deleted successfully")
    os.makedirs(local_dir)
    LOGGER.info(f"Flask app: Local Folder: {local_dir} - Created successfully")

create_new_folder(f'{os.getcwd()}/uploads')
create_new_folder(f'{os.getcwd()}/downloads')

if __name__ == '__main__':
    LOGGER.info("Staring Flask Module")
    assert aws_client.s3_bucket is not None
    app.run(host='0.0.0.0', debug=False, threaded=True)

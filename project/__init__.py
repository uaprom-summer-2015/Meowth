from flask import send_from_directory
import logging
import os
from project.application import create_app

app = create_app()


@app.route('/media/<path:path>')
def get_file(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)


# noinspection PyUnusedLocal
@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    logging.info(app.url_map)

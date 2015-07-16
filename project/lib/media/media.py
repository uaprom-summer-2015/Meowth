from project import app
from flask import send_from_directory

@app.route('/media/<path:path>')
def get_file(path):
    return send_from_directory('media', path)
from flask import send_from_directory, render_template
import logging
import os
from project.application import create_app
from project.bl import init_resource_registry

init_resource_registry()
app = create_app()


@app.route('/media/<path:path>')
def get_file(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)


# noinspection PyUnusedLocal
@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template("errors/413.html", error=error)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html", error=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html", error=error)

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    logging.info(app.url_map)

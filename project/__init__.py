from flask import send_from_directory, render_template, request
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
    return render_template("errors/413.html", error=error), 413


@app.errorhandler(404)
def page_not_found(error):
    path = request.path
    # go through each blueprint to find the prefix that matches the path
    # can't use request.blueprint since the routing didn't match anything
    for bp_name, bp in app.blueprints.items():
        if path.startswith(bp.url_prefix):
            # get the 404 handler registered by the blueprint
            handler = app.error_handler_spec.get(bp_name, {}).get(404)
            if handler is not None:
                # if a handler was found, return it's response
                return handler(error)
    # return a default response
    return render_template("errors/404.html", error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html", error=error), 500

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    logging.info(app.url_map)

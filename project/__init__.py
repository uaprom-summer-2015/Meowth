import logging
import os
from project.application import create_app
from project.bl import init_resource_registry

init_resource_registry()
app = create_app()


# noinspection PyUnusedLocal
@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    logging.info(app.url_map)

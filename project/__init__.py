import logging
import os
from project.application import create_app
from project.bl import init_resource_registry
from project.utils import inject_pagechunks

init_resource_registry()
app = create_app()

app.template_context_processors[None].append(inject_pagechunks)


# noinspection PyUnusedLocal
@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    logging.info(app.url_map)

import logging
import os
from project.application import create_app
from project.bl import init_resource_registry
from project.models import PageChunk

init_resource_registry()
app = create_app()





@app.context_processor
def inject_pagechunks():
    chunks = {chunk.name: chunk.text for chunk in PageChunk.query.all()}
    return {"pagechunks": chunks}


# noinspection PyUnusedLocal
@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    logging.info(app.url_map)

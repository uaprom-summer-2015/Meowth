import logging
from flask_mail import Mail
from flask_wtf.csrf import CsrfProtect
from project.celery import make_celery
from project import app
from project.models import PageChunk

celery = make_celery(app)
mail = Mail(app)
CsrfProtect(app)


@app.context_processor
def inject_pagechunks():
    chunks = {chunk.name: chunk.text for chunk in PageChunk.query.all()}
    return {"pagechunks": chunks}

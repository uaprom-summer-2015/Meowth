from project import PageChunk


def inject_pagechunks():
    chunks = {chunk.name: chunk.text for chunk in PageChunk.query.all()}
    return {"pagechunks": chunks}

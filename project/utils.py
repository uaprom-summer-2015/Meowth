import re

from project.models import PageChunk

contacts_map_coordinates = \
    re.compile(
        r".*"
        r"@(?P<latitude>\-?[\d\.]+),"
        r"(?P<longitude>\-?[\d\.]+),"
        r"(?P<zoom>[\d\.]+)z"
        r".*"
    )


def inject_pagechunks():
    chunks = {chunk.name: chunk.text for chunk in PageChunk.query.all()}
    return {"pagechunks": chunks}

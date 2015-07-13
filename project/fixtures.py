import json
import os
from pydoc import locate
from config import FIXTURES_DIR


def load_fixtures(session, filepath):
    filepath = os.path.join(FIXTURES_DIR, filepath)
    with open(filepath) as data_file:
        data = json.load(data_file)
        for o in data:
            cls = locate(o['model'])
            ins = cls(**o['fields'])
            session.add(ins)
        session.commit()

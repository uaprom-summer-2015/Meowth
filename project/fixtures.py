import importlib
import json
import os
from config import FIXTURES_DIR
from project.database import db_session as session


def import_class(what):
    modulename, classname = what.rsplit('.', 1)
    module = importlib.import_module(modulename)
    return getattr(module, classname)


def load_fixtures(filepath):
    filepath = os.path.join(FIXTURES_DIR, filepath)
    with open(filepath) as data_file:
        data = json.load(data_file)
        for entry in data:
            model_class = import_class(entry['model'])
            fixture_model = model_class(**entry['fields'])
            session.add(fixture_model)
        session.commit()

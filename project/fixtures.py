import json
import os
from config import FIXTURES_DIR
from project.database import db_session as session


def import_class(cl):
    d = cl.rfind(".")
    classname = cl[d+1:len(cl)]
    m = __import__(cl[0:d], globals(), locals(), [classname])
    return getattr(m, classname)


def load_fixtures(filepath):
    filepath = os.path.join(FIXTURES_DIR, filepath)
    with open(filepath) as data_file:
        data = json.load(data_file)
        for entry in data:
            model_class = import_class(entry['model'])
            fixture_model = model_class(**entry['fields'])
            session.add(fixture_model)
        session.commit()

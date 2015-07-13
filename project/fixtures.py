import json
import os
from pydoc import locate
from config import FIXTURES_DIR


def load_fixtures(session, filepath):
    filepath = os.path.join(FIXTURES_DIR, filepath)
    with open(filepath) as data_file:
        data = json.load(data_file)
        for entry in data:
            model_class = locate(entry['model'])
            fixture_model = model_class(**entry['fields'])
            session.add(fixture_model)
        session.commit()

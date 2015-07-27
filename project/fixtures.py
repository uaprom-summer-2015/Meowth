import importlib
import json
from project.extensions import db
from pathlib import Path


def import_class(what):
    modulename, classname = what.rsplit('.', 1)
    module = importlib.import_module(modulename)
    return getattr(module, classname)


def load_fixtures(fixtures_dir):
    fixtures = Path(fixtures_dir).glob("*.json")
    for fixture_file_path in fixtures:
        with fixture_file_path.open() as data_file:
            data = json.load(data_file)
            for entry in data:
                model_class = import_class(entry['model'])
                fixture_model = model_class(**entry['fields'])
                db.session.add(fixture_model)
    db.session.commit()

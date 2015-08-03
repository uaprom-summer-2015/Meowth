web: gunicorn project:app --log-file=-
worker: celery -A project.extensions.celery worker
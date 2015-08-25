from contextlib import contextmanager


@contextmanager
def disable_csrf(app):
    app.config['WTF_CSRF_ENABLED'] = False
    yield
    app.config['WTF_CSRF_ENABLED'] = True

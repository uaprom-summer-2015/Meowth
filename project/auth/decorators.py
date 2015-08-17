from flask import redirect, url_for, session, abort
from functools import wraps
from project.models import User


def login_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapped


def superuser_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        pk = session.get('user_id')
        if not pk:
            return redirect(url_for('auth.login'))
        u = User.query.get(pk)
        if not u or not u.is_superuser():
            abort(403)
        return func(*args, **kwargs)
    return wrapped

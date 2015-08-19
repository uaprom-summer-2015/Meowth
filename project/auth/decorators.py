from flask import redirect, url_for, session, abort
from functools import wraps
from project.models import User


def login_required(*, su_only=False):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            pk = session.get('user_id')
            if not pk:
                return redirect(url_for('auth.login'))
            u = User.query.get(pk)
            if not u:
                session.pop('user_id')
                session.pop('user_login')
                abort(403)
            if su_only and not u.is_superuser():
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return decorator

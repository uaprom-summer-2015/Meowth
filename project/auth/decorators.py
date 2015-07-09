from flask import g, redirect, url_for, session
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        print(session)
        if not session.get('user_id', None):
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapped





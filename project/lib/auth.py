from flask import session


def generate_random_string(n):
    import random
    import string
    charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.SystemRandom().choice(charset) for _ in range(n))


def get_user_from_session():
    from project.models import User
    pk = session.get('user_id')
    return User.query.get(pk) if pk else None

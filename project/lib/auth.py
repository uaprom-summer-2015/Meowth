def generate_random_password(n):
    import random
    import string
    charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.SystemRandom().choice(charset) for _ in range(n))
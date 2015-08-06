from contextlib import contextmanager

"""

Borrowed from
https://github.com/Orhideous/twicher/blob/master/twicher/utils.py

"""

COLORS = {
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'ORANGE': '\033[93m',
    'RED': '\033[91m',
    'END': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}


@contextmanager
def perform(
    name='perform',
    before=None,
    fail='Fail',
    after=None,
):
    format_args = dict(
        COLORS,
        name=name,
        before=before,
        fail=fail,
        after=after,
    )
    if (before is not None):
        print("{BLUE}[{name}]{END} {before}".format(**format_args))
    try:
        yield
    except Exception as e:
        print("{RED}[{name}]{END} {fail}".format(**format_args))
        print("{RED}[{name}]{END} Reason: {e}".format(e=e, **format_args))
        exit(1)
    else:
        if (after is not None):
            print("{GREEN}[{name}]{END} {after}".format(**format_args))

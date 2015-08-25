import re

contacts_map_coordinates = \
    re.compile(
        r".*"
        r"@(?P<latitude>\-?[\d\.]+),"
        r"(?P<longitude>\-?[\d\.]+),"
        r"(?P<zoom>[\d\.]+)z"
        r".*"
    )

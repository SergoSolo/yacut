from random import choices
from string import ascii_letters, digits


def get_unique_short_id():
    elements = ascii_letters + digits
    return ''.join(choices(elements, k=6))

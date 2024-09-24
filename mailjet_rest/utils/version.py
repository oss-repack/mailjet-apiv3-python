from typing import Tuple


VERSION: Tuple[int, int, int] = (1, 3, 3)


def get_version(version=None):
    '''
    Calculate package version based on a 3 item tuple.
    In addition verify that the tuple contains 3 items
    '''
    if version is None:
        version = VERSION
    else:
        assert len(version) == 3
    return "{}.{}.{}".format(*(x for x in version))

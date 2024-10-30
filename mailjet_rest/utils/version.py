VERSION = (1, 3, 5)


def get_version(version=None):
    """
    Calculate package version based on a 3 item tuple.
    In addition verify that the tuple contains 3 items
    """
    if version is None:
        version = VERSION
    if len(version) != 3:
        msg = "The tuple 'version' must contain 3 items"
        raise ValueError(msg)
    return "{}.{}.{}".format(*(x for x in version))

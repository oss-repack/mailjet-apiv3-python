VERSION = (1, 3, 3)


def get_version(version=None):
    """
    Calculate package version based on a 3 item tuple.
    In addition verify that the tuple contains 3 items
    """
    if version is None:
        version = VERSION
    if len(version) != 3:
        raise ValueError("The tuple 'version' must contain 3 items")
    return "{0}.{1}.{2}".format(*(x for x in version))

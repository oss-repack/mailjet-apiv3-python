#!/usr/bin/env python
from mailjet_rest.client import Client
from mailjet_rest.utils.version import get_version

__version__ = get_version()

__all__ = (Client, get_version)

# -*- coding: utf-8 -*-

"""
Integration test pytest configuration.

Re-exports fixtures from the package's internal ``tests/conftest.py`` (same
pattern as ``tests/conftest.py``).
"""

from {{ cookiecutter.package_name }}.tests.conftest import *

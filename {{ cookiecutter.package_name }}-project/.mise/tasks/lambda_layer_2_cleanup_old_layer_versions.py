# -*- coding: utf-8 -*-

from {{ cookiecutter.package_name }}.api import one

one.cleanup_old_layer_versions()

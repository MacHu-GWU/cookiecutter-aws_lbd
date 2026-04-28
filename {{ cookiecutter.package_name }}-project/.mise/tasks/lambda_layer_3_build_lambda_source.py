# -*- coding: utf-8 -*-

from {{ cookiecutter.package_name }}.api import one

one.build_lambda_source()

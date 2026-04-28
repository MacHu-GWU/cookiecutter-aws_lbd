# -*- coding: utf-8 -*-
# mise description="Build Lambda layer in Docker container (local build only, no upload/publish)"

from {{ cookiecutter.package_name }}.api import one

one.build_lambda_layer_only()

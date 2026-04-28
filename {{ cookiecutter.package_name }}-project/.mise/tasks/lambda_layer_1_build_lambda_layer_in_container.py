# -*- coding: utf-8 -*-
# mise description="Full Lambda layer pipeline: Build → Zip → Upload (S3) → Publish (AWS Lambda)"

from {{ cookiecutter.package_name }}.api import one

one.build_lambda_layer_in_container()

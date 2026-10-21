# -*- coding: utf-8 -*-

"""
Reject inputs the generated project cannot work with, before anything is written.
"""

import re
import sys

# The generated project pins requires-python, its classifiers and its CI matrix
# to these versions; mise.toml must use one of them.
# The Lambda runtime pins requires-python to one version (lambda_python_version
# in config/config-shared.json5), so the dev Python must match it.
SUPPORTED_PYTHON_VERSIONS = ["3.12"]

dev_python_version = "{{ cookiecutter.dev_python_version }}"

if dev_python_version not in SUPPORTED_PYTHON_VERSIONS:
    print(
        f"ERROR: dev_python_version must be one of "
        f"{', '.join(SUPPORTED_PYTHON_VERSIONS)}, got {dev_python_version!r}."
    )
    sys.exit(1)

# An AWS region code such as us-east-1, ap-southeast-2 or us-gov-west-1. It is
# written into config/config-<env>.json5 and the console URLs in mise.toml.
aws_region = "{{ cookiecutter.aws_region }}"

if not re.fullmatch(r"[a-z]{2}(-[a-z]+)+-\d+", aws_region):
    print(f"ERROR: aws_region must be an AWS region code such as us-east-1, got {aws_region!r}.")
    sys.exit(1)

# -*- coding: utf-8 -*-

"""
Run all infrastructure integration tests.
"""

if __name__ == "__main__":
    from {{ cookiecutter.package_name }}.tests import run_unit_test

    run_unit_test(
        __file__,
        is_folder=True,
    )

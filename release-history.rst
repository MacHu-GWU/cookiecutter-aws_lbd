.. _release_history:

Release and Version History
==============================================================================


Backlog (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**

0.2.1 (2026-10-21)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Built from seed @ ``93d7d4c``

**Breaking Changes**

- The generated project is rebuilt from scratch on the new seed: a multi-environment (``dev``, ``tst``, ``prd``) AWS Lambda project with a ``devops`` environment that owns the Lambda layer, a typed config loaded from ``config/*.json5`` locally and from SSM Parameter Store in Lambda, and two CDK stacks per environment (``infra`` for the IAM role, ``lbd`` for the functions and their triggers).
- The ``license`` choice ``Proprietary`` is now ``LicenseRef-Proprietary``, a valid SPDX expression written as is to ``pyproject.toml``.
- Removed the ``license_classifier``, ``codecov_token_field`` and ``readthedocs_token_field`` variables.

**Features and Improvements**

- New variable ``aws_region``: the region every environment deploys to. It is written into ``config/config-<env>.json5`` and every console URL in ``mise.toml`` and ``QUICK_LINKS.md``.
- New variable ``aws_account_prefix``: every bucket name derives from it, ``<prefix>-<dev|test|prod>-<region>-data`` for the data bucket of each environment and ``<prefix>-devops-<region>-artifacts`` for the Lambda layer artifacts.
- New variables ``devops_aws_account_id``, ``dev_aws_account_id``, ``tst_aws_account_id`` and ``prd_aws_account_id``: written into the git-ignored ``config/config-*-secret.json5`` files of the generated project, so they never enter its git history.
- The generated project comes with ``.env`` and every ``config/config-*-secret.json5`` already copied from their examples, ready to fill in.
- Input validation before generation: ``dev_python_version`` must be ``3.12`` (the Lambda runtime), ``aws_region`` must be a region code, ``aws_account_prefix`` must keep bucket names valid, and every account id must have 12 digits.
- New presets ``bmt`` and ``esc``, published as the ``preset/bmt`` and ``preset/esc`` branches.
- The generated project ships Claude Code skills for its toolchain and its Lambda and CDK conventions (``pywf-aws-lbd-base``, ``pywf-oss-*``, and one skill per key library).

**Miscellaneous**

- The template is now generated from the seed and checked by ``mise run sync`` (no leftover seed values, no unresolved placeholders, the template renders back into the seed, presets are valid), with the ``cctpl-*-cn`` Claude Code skills driving the maintenance workflow.
- The old ``preset/sanhe`` branch is no longer maintained.

0.1.1 (2025-04-28)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First Release

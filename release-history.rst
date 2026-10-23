.. _release_history:

Release and Version History
==============================================================================


Backlog (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.0.0 (2026-10-23)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Seed repo changes: `1.0.0 (2026-10-23) <https://github.com/MacHu-GWU/cookiecutter_aws_lbd_demo-project/blob/1.0.0/release-history-seed-repo.rst#100-2026-10-23>`__

**Features and Improvements**

- The template and its seed repo now share one version number, so a template version also names the seed state it was generated from. The version jumps from ``0.2.1`` to ``1.0.0`` for this reason only: generating a project works exactly as with ``0.2.1``, and no variable changed
- Every release entry in this file now starts with a link to the seed repo's own changelog (``release-history-seed-repo.rst``) at the seed's tag of the same version, which lists what newly generated projects get

**Minor Improvements**

- A published version is never overwritten: ``mise run publish-template`` creates the tag and the GitHub release in one step, refuses a version that already has a tag, and links the release to its changelog entry
- New ``mise run publish-presets`` regenerates the ``preset/*`` branches from the pushed ``main``; ``publish-template`` runs it last, and it can be rerun alone, for example after changing only ``presets/*.json``
- New ``mise run check-release``: before anything is pushed, checks the version is the same in the seed and in this repo, the template is current, the seed is pushed and tagged, and the changelog entry starts with the seed link
- New ``mise run check-version``, run by ``mise run sync``: the seed version is valid, documented in the seed's changelog, never recorded in the template's own ``release-history.rst``, and every link of the generated ``pywf-aws-lbd-base`` skill points at the seed's tag of that version
- New ``mise run e2e``: ``sync`` followed by ``try-template``, one command from the seed to a tested generated project
- The seed's tag of the same version records which seed commit a template version was built from; changelog entries no longer carry a ``Built from seed`` commit

**Bugfixes**

- The links of the generated ``pywf-aws-lbd-base`` skill now resolve: they point at the seed's ``1.0.0`` tag, while in ``0.2.1`` they pointed at a seed tag that did not exist
- A generated project's ``release-history.rst`` no longer starts with the template's own ``0.2.1`` release notes

**Miscellaneous**

- ``mise run sync`` copies the seed version into this repo's ``pyproject.toml`` and ``uv.lock``; the version is never edited here
- New ``cctpl-changelog-cn`` skill writes this file, replacing ``py-changelog``; the cctpl skills describe the shared version, the seed-only files, and the new release order


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

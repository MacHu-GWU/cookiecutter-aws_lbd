.. This file is the source of README.rst. Do not edit README.rst by hand:
   apply-template (mise run sync) renders it from this file.

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/cookiecutter-aws_lbd/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/cookiecutter-aws_lbd


``cookiecutter-aws_lbd``
==============================================================================


Overview
------------------------------------------------------------------------------
This template provides a ready-to-use structure for a Python code base that builds and deploys several `AWS Lambda <https://docs.aws.amazon.com/lambda/>`_ functions across several environments (``dev``, ``tst``, ``prd``), with the infrastructure in `AWS CDK <https://docs.aws.amazon.com/cdk/>`_ stacks built on `cdk_mate <https://github.com/MacHu-GWU/cdk_mate-project>`_. It generates a complete development environment that allows you to write, test, and deploy functions immediately.

**Key Features:**

- **Multi-environment config**: One JSON5 file per environment plus git-ignored secret files, loaded into a typed config from which every AWS resource name derives; deployed to SSM Parameter Store for the functions to read
- **Lambda layer**: The project dependencies built with uv for Linux without Docker, published once in a ``devops`` account, and pinned to a version per environment
- **Stacks as code**: Two sample stacks (``infra`` for the IAM role, ``lbd`` for the functions and their triggers) with stack exports, synth-only unit tests (no AWS call), and integration tests against deployed functions
- **One command per stack**: Generated ``mise run cdk-<synth|plan|up|down>-<env>-<stack>-stack`` tasks that print the CloudFormation console URL, then run one plain cdk command
- **Modern tooling**: Uses `mise-en-place <https://mise.jdx.dev/>`_ for tools (Python, Node.js, the cdk CLI, AWS CLI) and tasks, and `uv <https://docs.astral.sh/uv/>`_ for fast Python package management
- **Complete CI/CD**: Pre-configured GitHub Actions, CodeCov, and ReadTheDocs integration, plus Sphinx documentation
- **AI ready**: Ships Claude Code skills that know the project's toolchain, its Lambda and CDK conventions, and workflows


Disclaimer
------------------------------------------------------------------------------
The best practices implemented in this repository reflect my personal experience from developing `over 150 open source Python libraries <https://pypi.org/user/machugwu/>`_, 200+ proof-of-concept initiatives, 100+ enterprise-grade applications, and 50+ production systems. This workflow enables me to publish a new Python library to PyPI within an hour of conception. While these practices have proven effective for me, please use them at your own discretion.


Usage
------------------------------------------------------------------------------
Enter the following command to use the latest template version:

.. code-block:: bash

    pip install "cookiecutter>=2.6.0,<3.0.0" && cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws_lbd

To use a specific released version (see the `full list of releases <https://github.com/MacHu-GWU/cookiecutter-aws_lbd/releases>`_):

.. code-block:: bash

    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws_lbd --checkout tags/${version}

For example, to use ``1.0.0``, the latest version:

.. code-block:: bash

    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws_lbd --checkout tags/1.0.0

You'll then be prompted to provide the following information (defaults in parentheses):

.. code-block:: bash

    [1/14] Your Python package name, in snake case (e.g. my_package) (your_package_name): your_package_name
    [2/14] Your GitHub username, the owner of the new repo (your_github_username): your_github_username
    [3/14] Pick a license, as an SPDX expression for pyproject.toml, see https://choosealicense.com/ for details
      1 - MIT
      2 - AGPL-3.0-or-later
      3 - LicenseRef-Proprietary
      Choose from [1/2/3] (1): 1
    [4/14] Author name for pyproject.toml (Firstname Lastname): Firstname Lastname
    [5/14] Author email for pyproject.toml (firstname.lastname@email.com): firstname.lastname@email.com
    [6/14] Semantic Version, in {major}.{minor}.{micro} (e.g. 0.1.1) (0.1.1): 0.1.1
    [7/14] Python version for local development, in {major}.{minor} (e.g. 3.12) (3.12): 3.12
    [8/14] AWS region every environment (dev, tst, prd) deploys to (e.g. us-east-1) (us-east-1): us-east-1
    [9/14] Prefix of your AWS account names; bucket names derive from it, such as <prefix>-dev-<aws_region>-data and <prefix>-devops-<aws_region>-artifacts (your-aws-account-prefix): your-aws-account-prefix
    [10/14] GitHub token field. Read https://github.com/MacHu-GWU/home_secret_toml-project to learn how to set up your tokens using home_secret.toml (your_github_token_field): your_github_token_field
    [11/14] AWS account id of the devops environment, which owns the Lambda layer and the artifacts bucket (111122223333): 111122223333
    [12/14] AWS account id of the dev environment (123456789012): 123456789012
    [13/14] AWS account id of the tst environment (123456789012): 123456789012
    [14/14] AWS account id of the prd environment (123456789012): 123456789012

This will generate a repository structure similar to `cookiecutter_aws_lbd_demo-project <https://github.com/MacHu-GWU/cookiecutter_aws_lbd_demo-project>`_.

Once generated, navigate to your project directory and explore the available automation tasks:

.. code-block:: bash

    cd your_package_name-project
    mise tasks ls  # List all available tasks


Project Maintainer Note
------------------------------------------------------------------------------
**Project Architecture:**

- **Seed Repository**: `cookiecutter_aws_lbd_demo-project <https://github.com/MacHu-GWU/cookiecutter_aws_lbd_demo-project>`_ - A concrete, runnable project used as the source for template generation
- **Cookiecutter Template**: `cookiecutter-aws_lbd <https://github.com/MacHu-GWU/cookiecutter-aws_lbd>`_ - This repository

**Maintenance Workflow:**

This template is maintained using a "reverse engineering" approach, driven by Claude Code skills (``.claude/skills/cctpl-*-cn``):

1. Make changes in the Seed project (``cookiecutter_aws_lbd_demo-project``)
2. In the Seed, bump the version and record the changes in its own ``release-history-seed-repo.rst``. The Seed and this template share one version number, and the Seed's ``pyproject.toml`` is its only source
3. Run ``mise run e2e``: it converts the Seed into a template, checks it, applies it to this repo (version included), then generates a project and runs its tests and docs build
4. Commit and push the Seed, then tag it with ``mise run release`` in the Seed (push first: the tag goes on the latest commit of the Seed on GitHub)
5. Run ``/cctpl-release-cn`` to write this repo's changelog section, which links to the Seed's section of the same version, then ``mise run publish-template`` to publish the template to GitHub. A published version is never overwritten
6. Run ``/cctpl-verify-cn`` to verify the published template

**Toolchain:**

- **mise-en-place**: Task runner and tool version manager
- **uv**: Fast Python package installer and resolver
- **cookiecutter-maker**: Reverse-engineering tool that converts concrete projects into templates

For the full maintenance specification, see `cctpl-base-cn <./.claude/skills/cctpl-base-cn/SKILL.md>`_.
